"""
Grad-CAM (Gradient-Weighted Class Activation Mapping) Engine for 1D Time-Series CNNs.
Implements mathematically rigorous 1D Grad-CAM for temporal financial sequences.

Equations:
1. Gradients w.r.t Conv Feature Maps:
   g_{k, t}^c = ∂ y^c / ∂ A_{k, t}

2. Global-Average-Pooled Channel Importance Weights:
   α_k^c = (1 / L) * Σ_{t=1}^L g_{k, t}^c

3. 1D Temporal Class Activation Map:
   L_{Grad-CAM}^c(t) = ReLU( Σ_k α_k^c * A_{k, t} )

4. Normalized Saliency Heatmap:
   H(t) = (L^c(t) - min(L^c)) / (max(L^c) - min(L^c) + 1e-8)

Identifies:
- High-saliency temporal inflection intervals (e.g., breakdown at bar t-7, EMA cross at bar t-2).
- Channel importance ranking across indicator modalities.
- Perturbation response when masking salient temporal sub-windows.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional

import torch
import torch.nn.functional as F

from quantlens.models_cnn import (
    TimeSeriesConv1D, CNNModelManager, CNN_FEATURE_CHANNELS, LOOKBACK_WINDOW, CLASS_NAMES, DEVICE
)

logger = logging.getLogger(__name__)


class GradCAMEngine:
    """Computes genuine 1D Grad-CAM temporal attributions for TimeSeriesConv1D."""

    def __init__(self, cnn_manager: CNNModelManager):
        self.cnn_mgr = cnn_manager
        if self.cnn_mgr.model is None:
            self.cnn_mgr.load_model()
        self.model = self.cnn_mgr.model
        self.channel_names = CNN_FEATURE_CHANNELS

        self.activations: Optional[torch.Tensor] = None
        self.gradients: Optional[torch.Tensor] = None
        self._hook_handles = []
        self._register_hooks()

    def _register_hooks(self):
        """Registers forward and backward hooks on the last Conv1D layer (conv3)."""
        if self.model is None:
            return

        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0]

        target_layer = self.model.conv3
        h1 = target_layer.register_forward_hook(forward_hook)
        h2 = target_layer.register_full_backward_hook(backward_hook)
        self._hook_handles.extend([h1, h2])

    def remove_hooks(self):
        """Removes registered PyTorch hooks."""
        for h in self._hook_handles:
            h.remove()
        self._hook_handles = []

    def explain_window(
        self,
        window_t: np.ndarray,
        target_class: Optional[int] = None,
        candle_dates: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Computes 1D Grad-CAM temporal saliency for a given 30-bar lookback window (10, 30).
        Returns:
          - Predicted class and raw logits/probabilities
          - 30-day temporal heatmap (normalized [0, 1])
          - Top salient temporal windows (inflection points)
          - Indicator channel importance breakdown
          - Human-readable temporal interpretation
        """
        if self.model is None:
            self.cnn_mgr.load_model()
            self.model = self.cnn_mgr.model
            self._register_hooks()

        self.model.eval()
        self.activations = None
        self.gradients = None

        # Input shape: (1, 10, 30)
        x = torch.FloatTensor(window_t).unsqueeze(0).to(DEVICE)
        x.requires_grad_(True)

        logits = self.model(x)  # shape (1, 3)
        probs = torch.softmax(logits, dim=1).detach().cpu().numpy()[0]
        pred_class = int(np.argmax(probs))

        if target_class is None:
            target_class = pred_class

        score = logits[0, target_class]

        self.model.zero_grad()
        score.backward(retain_graph=True)

        # Retrieve captured activations & gradients from conv3: shape (1, 64, 30)
        activations = self.activations.detach().cpu().numpy()[0]  # shape (64, 30)
        gradients = self.gradients.detach().cpu().numpy()[0]     # shape (64, 30)

        # 1. Global average pooling of gradients over time length L: shape (64,)
        weights = np.mean(gradients, axis=1)

        # 2. Weighted sum of activation maps: shape (30,)
        cam = np.zeros(activations.shape[1], dtype=np.float32)
        for k, w in enumerate(weights):
            cam += w * activations[k]

        # 3. ReLU to discard features that decrease target class score
        cam = np.maximum(cam, 0.0)

        # 4. Normalize to [0, 1]
        cam_min, cam_max = np.min(cam), np.max(cam)
        if cam_max - cam_min > 1e-8:
            heatmap = (cam - cam_min) / (cam_max - cam_min)
        else:
            heatmap = np.ones_like(cam) / len(cam)

        heatmap = [round(float(v), 4) for v in heatmap]

        # 5. Extract indicator channel weights across time
        # Channel-level sensitivity: sum of absolute gradient * activation across time for each channel in input
        x_grad = x.grad.detach().cpu().numpy()[0]  # shape (10, 30)
        channel_saliency = np.mean(np.abs(x_grad * window_t), axis=1)  # shape (10,)
        if np.sum(channel_saliency) > 0:
            channel_norm = channel_saliency / np.sum(channel_saliency)
        else:
            channel_norm = np.ones(10) / 10.0

        channel_ranking = [
            {
                "channel": self.channel_names[i],
                "attribution": round(float(channel_norm[i]), 4),
                "rank": int(r + 1)
            }
            for r, i in enumerate(np.argsort(-channel_norm))
        ]

        # 6. Temporal Salient Intervals (bars where saliency >= 0.60)
        high_saliency_bars = []
        for t_idx, val in enumerate(heatmap):
            bar_offset = t_idx - (LOOKBACK_WINDOW - 1)  # e.g., -29 to 0 (0 is current candle)
            date_label = candle_dates[t_idx] if candle_dates and t_idx < len(candle_dates) else f"T{bar_offset}"
            if val >= 0.60:
                high_saliency_bars.append({
                    "step": t_idx,
                    "bar_offset": bar_offset,
                    "date": date_label,
                    "saliency": val,
                    "intensity": "Peak" if val >= 0.85 else "Strong"
                })

        # Identify most critical temporal window
        if high_saliency_bars:
            top_bar = max(high_saliency_bars, key=lambda b: b["saliency"])
            narrative = (
                f"Grad-CAM identifies peak temporal saliency ({top_bar['saliency'] * 100:.1f}%) "
                f"at bar offset {top_bar['bar_offset']} ({top_bar['date']}). "
                f"The 1D convolutional feature map confirms the {CLASS_NAMES[target_class]} signal was primarily triggered "
                f"by multi-day indicator momentum centered on channels '{channel_ranking[0]['channel']}' and '{channel_ranking[1]['channel']}'."
            )
        else:
            narrative = (
                f"Grad-CAM activations are uniformly distributed across the 30-day sequence. "
                f"Leading predictive channel: '{channel_ranking[0]['channel']}' ({channel_ranking[0]['attribution'] * 100:.1f}%)."
            )

        return {
            "model": "TimeSeriesConv1D",
            "target_class": CLASS_NAMES[target_class],
            "target_class_idx": target_class,
            "predicted_class": CLASS_NAMES[pred_class],
            "confidence": round(float(probs[pred_class]), 4),
            "class_probabilities": {CLASS_NAMES[i]: round(float(probs[i]), 4) for i in range(3)},
            "sequence_length": LOOKBACK_WINDOW,
            "temporal_heatmap": heatmap,
            "high_saliency_intervals": high_saliency_bars,
            "channel_attributions": channel_ranking,
            "narrative": narrative
        }

    def explain_by_date(
        self,
        target_date: str,
        target_class: Optional[int] = None
    ) -> Dict[str, Any]:
        """Explains historical candle window aligned with exact trading date."""
        if self.cnn_mgr.X_all is None:
            self.cnn_mgr.load_model()

        dates = self.cnn_mgr.dates
        target_str = str(target_date)[:10]

        if target_str in dates:
            idx = dates.index(target_str)
        else:
            idx = len(dates) - 1

        window = self.cnn_mgr.X_all[idx]
        window_dates = dates[max(0, idx - LOOKBACK_WINDOW + 1) : idx + 1]
        while len(window_dates) < LOOKBACK_WINDOW:
            window_dates.insert(0, "pre-history")

        res = self.explain_window(window, target_class=target_class, candle_dates=window_dates)
        res["target_date"] = dates[idx]
        return res
