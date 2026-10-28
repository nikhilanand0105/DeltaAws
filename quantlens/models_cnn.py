"""
Model C: 1D Time-Series Convolutional Neural Network (TimeSeriesConv1D) for QuantLens-XAI.
Provides a temporal deep-learning architecture operating on sequential market sliding windows.
Enables genuine Grad-CAM temporal feature attribution by exposing 1D convolutional feature maps.

Architecture:
- Input: (batch_size, channels=10, sequence_length=30)
- Conv1D(10 -> 32, kernel=3, padding=1) + BatchNorm1d + ReLU
- Conv1D(32 -> 64, kernel=3, padding=1) + BatchNorm1d + ReLU
- Conv1D(64 -> 64, kernel=3, padding=1) + BatchNorm1d + ReLU [Grad-CAM Hook Layer]
- AdaptiveAvgPool1d(1) + Dropout(0.25)
- Linear(64, 3) -> Logits [SELL=0, HOLD=1, BUY=2]
Strictly adheres to chronological splitting with zero look-ahead bias.
"""

import os
import json
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from quantlens.data_loader import load_historical_ohlcv
from quantlens.feature_engineering import calculate_rsi, calculate_macd, calculate_bollinger_bands

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

CLASS_NAMES = ["SELL", "HOLD", "BUY"]
DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

CNN_FEATURE_CHANNELS = [
    "close_to_open_ratio",
    "ema_ratio",
    "rsi_norm",
    "macd_hist_norm",
    "vol_ratio",
    "atr_pct",
    "ret_5d",
    "bb_pct_b",
    "high_low_spread",
    "obv_norm"
]

LOOKBACK_WINDOW = 30  # 30 daily bars lookback


def extract_cnn_channel_matrix(df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
    """
    Extracts 10 normalized, stationary financial indicator channels from raw OHLCV bars.
    Guarantees no future data leakage by strictly using rolling causal calculations.
    """
    data = df.copy()
    close = data["close"]
    open_p = data["open"]
    high = data["high"]
    low = data["low"]
    volume = data["volume"]

    # 1. Close-to-Open return
    c_o = ((close - open_p) / open_p.replace(0, np.nan)).fillna(0.0)

    # 2. EMA 10 vs EMA 30 ratio
    ema10 = close.ewm(span=10, adjust=False).mean()
    ema30 = close.ewm(span=30, adjust=False).mean()
    ema_ratio = ((ema10 - ema30) / close.replace(0, np.nan)).fillna(0.0)

    # 3. Normalized RSI (scaled to [-1, 1])
    rsi = calculate_rsi(close, 14)
    rsi_norm = ((rsi - 50.0) / 50.0).clip(-1.0, 1.0)

    # 4. Normalized MACD Histogram
    _, _, macd_hist = calculate_macd(close, 12, 26, 9)
    macd_hist_norm = (macd_hist / close.replace(0, np.nan)).fillna(0.0)

    # 5. Volume ratio relative to 20-day SMA
    vol_sma20 = volume.rolling(20).mean().replace(0, np.nan)
    vol_ratio = ((volume - vol_sma20) / vol_sma20).clip(-2.0, 5.0).fillna(0.0)

    # 6. ATR as percentage of price
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().fillna(0.0)
    atr_pct = (atr / close.replace(0, np.nan)).fillna(0.0)

    # 7. 5-day trailing return
    ret_5d = ((close - close.shift(5)) / close.shift(5).replace(0, np.nan)).clip(-0.5, 0.5).fillna(0.0)

    # 8. Bollinger %B centered at 0
    _, _, _, _, pct_b = calculate_bollinger_bands(close, 20, 2.0)
    bb_pct_b = (pct_b - 0.5).clip(-1.0, 1.0)

    # 9. High-Low normalized spread
    hl_spread = ((high - low) / close.replace(0, np.nan)).clip(0.0, 0.2).fillna(0.0)

    # 10. Normalized OBV change
    direction = np.sign(close.diff().fillna(0))
    obv = (direction * volume).cumsum()
    obv_sma20 = obv.rolling(20).mean()
    obv_std20 = obv.rolling(20).std().replace(0, np.nan)
    obv_norm = ((obv - obv_sma20) / obv_std20).clip(-3.0, 3.0).fillna(0.0)

    channel_df = pd.DataFrame({
        "close_to_open_ratio": c_o,
        "ema_ratio": ema_ratio,
        "rsi_norm": rsi_norm,
        "macd_hist_norm": macd_hist_norm,
        "vol_ratio": vol_ratio,
        "atr_pct": atr_pct,
        "ret_5d": ret_5d,
        "bb_pct_b": bb_pct_b,
        "high_low_spread": hl_spread,
        "obv_norm": obv_norm
    }).fillna(0.0)

    return channel_df[CNN_FEATURE_CHANNELS].values, CNN_FEATURE_CHANNELS


def generate_cnn_sliding_windows(
    df: pd.DataFrame,
    window_size: int = LOOKBACK_WINDOW,
    future_return_threshold: float = 0.015
) -> Tuple[np.ndarray, np.ndarray, List[str], List[str]]:
    """
    Constructs chronological sliding window sequences:
    X: shape (N, channels, window_size) -> (N, 10, 30)
    y: shape (N,) with classes 0: SELL, 1: HOLD, 2: BUY based on 5-day future return.
    Returns:
      X_tensor, y_array, date_labels, channel_names
    """
    channel_matrix, channel_names = extract_cnn_channel_matrix(df)
    close = df["close"].values
    dates = [str(d)[:10] for d in df["date"]] if "date" in df.columns else [f"day_{i}" for i in range(len(df))]

    n_samples = len(df)
    X_list = []
    y_list = []
    target_dates = []

    # Requires window_size lookback and 5-day forward target
    for i in range(window_size - 1, n_samples - 5):
        window = channel_matrix[i - window_size + 1 : i + 1]  # shape (30, 10)
        # Transpose to (channels, sequence_length) for PyTorch Conv1d
        window_t = window.T  # shape (10, 30)
        X_list.append(window_t)

        current_close = close[i]
        future_close = close[i + 5]
        ret_5d = (future_close - current_close) / current_close if current_close > 0 else 0.0

        if ret_5d >= future_return_threshold:
            label = 2  # BUY
        elif ret_5d <= -future_return_threshold:
            label = 0  # SELL
        else:
            label = 1  # HOLD

        y_list.append(label)
        target_dates.append(dates[i])

    X_arr = np.array(X_list, dtype=np.float32)  # shape (N, 10, 30)
    y_arr = np.array(y_list, dtype=np.int64)

    return X_arr, y_arr, target_dates, channel_names


class TimeSeriesConv1D(nn.Module):
    """
    1D Convolutional Neural Network for financial sequence classification.
    Allows capturing multi-scale temporal motifs (cross-overs, volume surges, trend breaks).
    The conv3 layer acts as the target feature map for Grad-CAM activation weighting.
    """
    def __init__(self, in_channels: int = 10, num_classes: int = 3):
        super(TimeSeriesConv1D, self).__init__()
        self.conv1 = nn.Conv1d(in_channels, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(32)
        self.relu1 = nn.ReLU()

        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(64)
        self.relu2 = nn.ReLU()

        # Target feature map layer for Grad-CAM
        self.conv3 = nn.Conv1d(64, 64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(64)
        self.relu3 = nn.ReLU()

        self.pool = nn.AdaptiveAvgPool1d(1)
        self.dropout = nn.Dropout(0.25)
        self.fc = nn.Linear(64, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (B, 10, 30)
        h = self.relu1(self.bn1(self.conv1(x)))
        h = self.relu2(self.bn2(self.conv2(h)))
        h = self.relu3(self.bn3(self.conv3(h)))
        pooled = self.pool(h).squeeze(-1)  # (B, 64)
        logits = self.fc(self.dropout(pooled))  # (B, 3)
        return logits


class CNNModelManager:
    """Manages training, inference, and persistence for Model C (TimeSeriesConv1D)."""

    def __init__(self, symbol: str = "RELIANCE"):
        self.symbol = symbol.upper().replace(".NS", "")
        self.model_path = os.path.join(MODELS_DIR, f"pytorch_cnn_{self.symbol.lower()}.pt")
        self.meta_path = os.path.join(MODELS_DIR, f"models_meta_cnn_{self.symbol.lower()}.json")
        self.model: Optional[TimeSeriesConv1D] = None
        self.eval_metrics: Dict[str, Any] = {}
        self.dates: List[str] = []
        self.X_all: Optional[np.ndarray] = None
        self.y_all: Optional[np.ndarray] = None
        self.channel_names = CNN_FEATURE_CHANNELS

    def load_model(self) -> bool:
        if os.path.exists(self.model_path):
            try:
                self.model = TimeSeriesConv1D(in_channels=len(CNN_FEATURE_CHANNELS), num_classes=3).to(DEVICE)
                state_dict = torch.load(self.model_path, map_location=DEVICE)
                self.model.load_state_dict(state_dict)
                self.model.eval()

                if os.path.exists(self.meta_path):
                    with open(self.meta_path, "r") as f:
                        meta = json.load(f)
                        self.eval_metrics = meta.get("metrics", {})

                # Load dataset for indexing
                df = load_historical_ohlcv(self.symbol)
                self.X_all, self.y_all, self.dates, self.channel_names = generate_cnn_sliding_windows(df)
                return True
            except Exception as e:
                logger.error(f"Failed to load CNN model: {e}")
                return False
        return False

    def train_and_evaluate(self, force_retrain: bool = False, epochs: int = 35) -> Dict[str, Any]:
        """
        Trains TimeSeriesConv1D using strict chronological splits: 70% train, 15% val, 15% test.
        Computes Accuracy, Precision, Recall, Macro F1, and Multiclass ROC-AUC on untouched test set.
        """
        if not force_retrain and self.load_model():
            return {
                "symbol": self.symbol,
                "model": "TimeSeriesConv1D",
                "status": "cached",
                "metrics": self.eval_metrics
            }

        df = load_historical_ohlcv(self.symbol)
        X, y, dates, channel_names = generate_cnn_sliding_windows(df)
        self.X_all = X
        self.y_all = y
        self.dates = dates
        self.channel_names = channel_names

        n_samples = len(X)
        train_end = int(n_samples * 0.70)
        val_end = int(n_samples * 0.85)

        X_train, y_train = X[:train_end], y[:train_end]
        X_val, y_val = X[train_end:val_end], y[train_end:val_end]
        X_test, y_test = X[val_end:], y[val_end:]

        train_ds = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
        val_ds = TensorDataset(torch.FloatTensor(X_val), torch.LongTensor(y_val))
        test_ds = TensorDataset(torch.FloatTensor(X_test), torch.LongTensor(y_test))

        train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=64, shuffle=False)
        test_loader = DataLoader(test_ds, batch_size=64, shuffle=False)

        model = TimeSeriesConv1D(in_channels=len(channel_names), num_classes=3).to(DEVICE)

        # Calculate inverse frequency class weights to balance dataset
        classes, counts = np.unique(y_train, return_counts=True)
        total_counts = len(y_train)
        weights = [total_counts / (len(classes) * c) for c in counts]
        class_weights = torch.FloatTensor(weights).to(DEVICE)

        criterion = nn.CrossEntropyLoss(weight=class_weights)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.002, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=5)

        best_val_loss = float("inf")
        best_state = None

        for epoch in range(epochs):
            model.train()
            for bx, by in train_loader:
                bx, by = bx.to(DEVICE), by.to(DEVICE)
                optimizer.zero_grad()
                logits = model(bx)
                loss = criterion(logits, by)
                loss.backward()
                optimizer.step()

            # Validation
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for bx, by in val_loader:
                    bx, by = bx.to(DEVICE), by.to(DEVICE)
                    out = model(bx)
                    val_loss += criterion(out, by).item() * len(bx)
            val_loss /= len(val_ds)
            scheduler.step(val_loss)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        if best_state is not None:
            model.load_state_dict(best_state)

        # Evaluation on untouched test split
        model.eval()
        test_preds = []
        test_probs = []
        test_targets = []

        with torch.no_grad():
            for bx, by in test_loader:
                bx = bx.to(DEVICE)
                out = model(bx)
                probs = torch.softmax(out, dim=1).cpu().numpy()
                preds = np.argmax(probs, axis=1)

                test_probs.extend(probs)
                test_preds.extend(preds)
                test_targets.extend(by.numpy())

        test_probs = np.array(test_probs)
        test_preds = np.array(test_preds)
        test_targets = np.array(test_targets)

        acc = float(accuracy_score(test_targets, test_preds))
        prec = float(precision_score(test_targets, test_preds, average="macro", zero_division=0))
        rec = float(recall_score(test_targets, test_preds, average="macro", zero_division=0))
        f1 = float(f1_score(test_targets, test_preds, average="macro", zero_division=0))

        try:
            auc = float(roc_auc_score(test_targets, test_probs, multi_class="ovr", average="macro"))
        except Exception:
            auc = 0.50

        metrics = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(auc, 4),
            "samples_train": len(X_train),
            "samples_val": len(X_val),
            "samples_test": len(X_test),
            "device": str(DEVICE),
            "channels": channel_names,
            "lookback_window": LOOKBACK_WINDOW
        }

        # Save artifacts
        torch.save(model.state_dict(), self.model_path)
        meta = {
            "symbol": self.symbol,
            "model": "TimeSeriesConv1D",
            "channels": channel_names,
            "metrics": metrics
        }
        with open(self.meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        self.model = model
        self.eval_metrics = metrics
        return meta

    def predict_window(self, window_t: np.ndarray) -> Tuple[int, float, List[float]]:
        """
        Inference on a single window (10, 30).
        Returns predicted class index, confidence, and class probabilities list.
        """
        if self.model is None:
            self.load_model()
            if self.model is None:
                raise RuntimeError("Model C (CNN) not trained or loaded.")

        self.model.eval()
        with torch.no_grad():
            t = torch.FloatTensor(window_t).unsqueeze(0).to(DEVICE)  # shape (1, 10, 30)
            logits = self.model(t)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
            pred_class = int(np.argmax(probs))
            conf = float(probs[pred_class])

        return pred_class, conf, [float(p) for p in probs]
