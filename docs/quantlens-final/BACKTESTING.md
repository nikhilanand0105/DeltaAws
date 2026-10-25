# QuantLens-XAI: Deterministic Event-Driven Backtesting Engine

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Reference:** Research Proposal Slide 10

---

## 1. Engine Design & Philosophy

The QuantLens backtesting engine (`quantlens/backtest_engine.py`) provides deterministic, bar-by-bar historical evaluation of trading strategies. Unlike simplistic vectorized backtests that assume instantaneous execution at closing prices, QuantLens simulates real-world execution constraints:
1. **Event-Driven Simulation**: Trades are evaluated chronologically bar-by-bar.
2. **Deterministic Slippage**: Modeled at $0.05\%$ adverse execution shift.
3. **Brokerage & Turnover Fees**: Modeled at $0.05\%$ of gross transaction value.
4. **Finite Capital Allocation**: Enforces user-specified allocation caps (e.g., $10\%$ max capital per trade).
5. **Multi-Condition Exit Evaluation**: Simultaneously monitors Stop-Loss, Take-Profit, and reverse indicator crossovers.

---

## 2. Quantitative Financial KPIs (Slide 10)

For any tested strategy, the engine computes:

### 2.1 Cumulative Return (%)
$$\text{Cumulative Return} = \frac{\text{Final Portfolio Value} - \text{Initial Capital}}{\text{Initial Capital}} \times 100\%$$

### 2.2 Annualized Sharpe Ratio
Measures excess return per unit of total risk assuming 252 trading days per year:
$$\text{Sharpe Ratio} = \sqrt{252} \times \frac{\bar{r} - r_f}{\sigma_r}$$
Where $r_f$ is the risk-free rate (assumed $6.0\%$ annualized for Indian sovereign debt).

### 2.3 Sortino Ratio
Measures excess return per unit of downside risk, penalizing only negative volatility:
$$\text{Sortino Ratio} = \sqrt{252} \times \frac{\bar{r} - r_f}{\sigma_d}, \quad \text{where } \sigma_d = \sqrt{\frac{1}{N} \sum_{t=1}^N \min(0, r_t - r_f)^2}$$

### 2.4 Maximum Drawdown (MDD)
The peak-to-trough decline across the simulation:
$$\text{MDD} = \max_{t \in [0, T]} \left( \frac{\max_{s \le t} \text{Equity}_s - \text{Equity}_t}{\max_{s \le t} \text{Equity}_s} \right) \times 100\%$$

### 2.5 Win Rate & Profit Factor
$$\text{Win Rate} = \frac{\text{Number of Winning Trades}}{\text{Total Completed Trades}} \times 100\%$$
$$\text{Profit Factor} = \frac{\sum \text{Gross Gains from Winning Trades}}{\sum |\text{Gross Losses from Losing Trades}|}$$

---

## 3. Backtest Benchmark: Demo Strategy on RELIANCE

Running the faculty demonstration strategy:
- **Symbol:** RELIANCE (Daily)
- **Rules:** Buy on EMA(10) > EMA(30) with RSI < 65; Exit on reverse cross, 2% Stop Loss, or 4% Take Profit; 10% allocation.
- **Initial Capital:** ₹1,00,000 INR

### Output Metrics Summary
- **Cumulative Net Profit:** $+₹200.00$ ($+0.20\%$)
- **Annualized Sharpe Ratio:** $-1.17$
- **Sortino Ratio:** $-0.55$
- **Maximum Drawdown:** $1.44\%$
- **Total Trades Executed:** 27 completed trades
- **Win Rate:** $37.04\%$
- **Winning Trades:** 10
- **Losing Trades:** 17
- **Total Exchange & Brokerage Fees Paid:** ₹114.20
- **Primary Exit Driver:** Stop-loss protection prevented large catastrophic drawdowns during rangebound chop, maintaining a remarkably tight maximum drawdown of only $1.44\%$.
