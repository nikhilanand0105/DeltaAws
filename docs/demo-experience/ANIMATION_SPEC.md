# QuantLens-XAI — Animation & Motion Design Specification

## 1. Design Philosophy

Motion in QuantLens-XAI is designed for **technical credibility, visual clarity, and responsiveness**. Animations reinforce cognitive understanding of quantitative data pipelines without introducing frivolous or childish distractions.

### Core Principles
1. **Computational Honesty:** Animations never misrepresent execution state. Fast computations are presented immediately, followed by brief, satisfying staggered reveals.
2. **Smooth 60 FPS Performance:** All motion utilizes hardware-accelerated CSS properties (`transform: translate3d()`, `opacity`, `filter`). No layout thrashing or unbounded canvas rendering.
3. **Accessibility First:** Respects `prefers-reduced-motion` and provides an explicit **"Skip Animations"** toggle for rapid faculty presentations.

---

## 2. Animation Token Library

| Token Name | Value | Purpose |
| :--- | :--- | :--- |
| `--motion-duration-instant` | `100ms` | Micro-interactions (hover, active button presses) |
| `--motion-duration-fast` | `250ms` | Card expansions, tab transitions, pill reveals |
| `--motion-duration-medium` | `450ms` | Panel cross-fades, chart container reveals |
| `--motion-duration-deliberate` | `700ms` | Staggered pipeline stage illumination, counter count-ups |
| `--motion-ease-standard` | `cubic-bezier(0.4, 0.0, 0.2, 1)` | General UI movement |
| `--motion-ease-enter` | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Incoming elements (fade and slide up) |
| `--motion-ease-exit` | `cubic-bezier(0.4, 0.0, 1, 1)` | Dismissals and collapse transitions |
| `--motion-ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Checkmark pop, badge lock-in |

---

## 3. Scene-by-Scene Animation Choreography

### 3.1 Strategy Run Trigger & Mission Control Launch
- **Trigger:** Click on `ANALYZE & RUN STRATEGY` button.
- **Button Effect:**
  - Scale: `scale(0.97)` on active press (100ms).
  - Radial pulse ring expands: `opacity: 0.8 -> 0`, `transform: scale(1.6)` (400ms).
- **View Transition:**
  - Input screen fades out: `opacity: 1 -> 0`, `transform: scale(0.98)` (250ms).
  - Mission Control dashboard fades in: `opacity: 0 -> 1`, `transform: translateY(12px) -> 0` (350ms, ease-enter).

### 3.2 Pipeline Stage Illumination (Left Panel)
- **Status States:**
  - `WAITING`: Dim slate color (`#4b5563`), opacity `0.45`.
  - `RUNNING`: Electric cyan border (`#06b6d4`), subtle breathing glow (`box-shadow: 0 0 16px rgba(6, 182, 212, 0.35)`), pulsing dot (800ms infinite loop).
  - `COMPLETED`: Smooth color transition to Emerald Green (`#10b981`), checkmark icon scales from `0.6 -> 1.0` with spring bounce (300ms). Connecting trace line animates height from `0% -> 100%` (250ms).
  - `CACHED / FALLBACK`: Warm amber accent (`#f59e0b`), steady border glow.
  - `FAILED`: Controlled crimson red (`#ef4444`), gentle horizontal shake (`translateX(-3px) -> translateX(3px)`, 3 cycles, 200ms).

### 3.3 Rule Extraction Animation (Center Panel)
- **Trigger:** Structured parse completion from local Ollama.
- **Motion:**
  - Input text phrases highlight with tinted pill borders.
  - Extracted rule cards slide down from the token mapping area into the structured rule grid with a 60ms stagger per card.
  - Arrow connectors draw in using SVG `stroke-dashoffset` transition (400ms).

### 3.4 Risk Intelligence Warning Reveal
- **Trigger:** Identification of regime warnings (e.g. choppy market whipsaw).
- **Motion:**
  - Warning banner expands accordion-style: `max-height: 0 -> 240px`, `opacity: 0 -> 1` (350ms, ease-enter).
  - Amber warning icon pulses once: `scale(1.2) -> scale(1.0)` (250ms).

### 3.5 AI Advisor Progressive Reveal
- **Trigger:** Strategy validation approval.
- **Motion:**
  - Advisory paragraphs reveal line-by-line with a gentle upward slide (`translateY(8px) -> 0`, opacity `0 -> 1`, 50ms stagger per section).
  - Contextual Q&A answer accordion expands smoothly upon user click (200ms).

### 3.6 XGBoost vs PyTorch Showdown
- **Trigger:** Model inference completion.
- **Motion:**
  - Left card (XGBoost) slides in from `translateX(-24px) -> 0` (400ms).
  - Right card (PyTorch MLP) slides in from `translateX(24px) -> 0` (400ms).
  - Central Consensus Badge scales in: `scale(0.8) -> scale(1.0)` with a subtle cyan ring pulse (300ms).

### 3.7 SHAP & LIME Feature Attributions
- **Trigger:** Explainability computation load.
- **Motion:**
  - Horizontal attribution bars expand from `width: 0%` to their calculated magnitude:
    - Positive contribution: Emerald green (`#10b981`), expanding rightward.
    - Negative contribution: Coral red (`#f43f5e`), expanding leftward.
    - Duration: 600ms, `cubic-bezier(0.16, 1, 0.3, 1)`.
  - Feature Cross-Linking: Clicking a feature bar instantly highlights that feature across all charts with a persistent cyan outline (`box-shadow: 0 0 12px rgba(6, 182, 212, 0.5)`).

### 3.8 Guided Backtest & Signal Replay
- **Trigger:** Playback start (`Play` button or `Next Signal`).
- **Motion:**
  - Candlestick cursor marker moves smoothly across time bars.
  - Signal Markers: BUY triangle pops in above candle with green ring; SELL triangle pops below candle with red ring.
  - Financial KPI Counters: Numbers tick up dynamically from 0 to final calculated values (e.g. `0% -> +0.20%`, `0 -> 27 trades`) over 800ms using a linear interpolation easing.

### 3.9 Deployment Transition to Paper Broker
- **Trigger:** Click on **"DEPLOY TO QUANTLENS PAPER BROKER"**.
- **Motion:**
  - Research cards scale down and dock into a compact floating pill (400ms).
  - Floating pill translates diagonally down-right toward the broker console (`transform: translate3d(40vw, 30vh, 0) scale(0.6)`).
  - Full-screen Paper Broker console reveals: `opacity: 0 -> 1`, `scale(0.98) -> scale(1.0)` (450ms).
  - Virtual account balance (`₹1,00,000.00`) illuminates with count-up animation.

### 3.10 Simulated Order Execution Overlay
- **Trigger:** Simulated trade fill during historical replay.
- **Motion:**
  - Relevant chart candle flashes white-cyan briefly (150ms).
  - Compact Order Execution Card slides in at top right:
    `PAPER BUY EXECUTED: RELIANCE | 7 Shares @ ₹1,294.25`
  - Holds for 2.5 seconds, then slides out to the right (`translateX(110%)`).
  - Cash and Portfolio equity counters update immediately with subtle green (gain) or amber/red (spend/loss) flash.

---

## 4. Reduced-Motion Mode & Presentation Skip Controls

When `prefers-reduced-motion: reduce` is active OR the user enables **"Skip Animations"** in the top bar:
- All CSS transitions default to `duration: 0.01ms !important`.
- Number counters render their target values instantly without counting up.
- Staggered reveals appear immediately with `opacity: 1`.
- The presentation progresses instantly without blocking faculty review.
