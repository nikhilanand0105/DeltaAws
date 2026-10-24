# DA3 Video Demonstration: Website Navigation Guide
## Course: Cloud Architecture Design (BCSE355L) — Academic Year 2026–27
**Target Application**: Live AWS-Hosted Algorithmic Trading System  
**Live Production URL**: `https://13-203-204-25.sslip.io/dashboard`  
**SSL Certificate**: Let's Encrypt Authority X3 / YE2 (Browser-Trusted TLSv1.3)  

---

## 1. Initial Access & URL Verification

1. Open your browser (Google Chrome or Brave recommended) and navigate to:
   ```
   https://13-203-204-25.sslip.io/dashboard
   ```
2. Verify that the address bar displays a solid padlock icon (`https://`).
3. If clicked, the certificate viewer will confirm:
   - **Common Name (CN)**: `13-203-204-25.sslip.io`
   - **Issuer**: Let's Encrypt
   - **Validity**: Active through January 2027
   - **Status**: Zero browser security warnings or self-signed certificate alerts.

---

## 2. Navigating the 7 Dashboard Tabs

The navigation bar located at the top of the interface provides access to the application's core functional modules:

```
[ Accounts ]  [ Trades & PnL ]  [ Performance Analytics ]  [ Trade Logs ]  [ Email Verification ]  [ Alert Playground ]  [ Global Settings ]
```

---

### Step-by-Step Demonstration Actions

### A. The "Accounts" Tab (Default Landing View)
- **Menu Label**: `Accounts` (`data-tab="accounts-tab"`, URL hash: `#accounts`)
- **What it Displays**:
  - Four pre-configured algorithmic trading paper accounts:
    1. **Alpha Momentum Fund (Paper)** (ID: 1) — 50x Leverage, 80% Buffer.
    2. **Delta Grid & Arbitrage (Paper)** (ID: 2) — 20x Leverage, 60% Buffer.
    3. **Institutional Swing Pool (Paper)** (ID: 3) — 10x Leverage, Fixed Margin $50 USD.
    4. **Retail Algorithmic Vault (Paper)** (ID: 4) — 25x Leverage, 70% Buffer.
- **Actions to Perform on Video**:
  1. Hover your cursor over the *Alpha Momentum Fund* card.
  2. Point out the configured leverage (**50x**) and sizing method (**Percentage Allocation**).
  3. Click the secondary button: **`Check Balance`** on Account #1.
  4. An asynchronous request is dispatched to `/api/accounts/1/balance`. A non-blocking toast notification appears in the top-right corner confirming:
     > `Alpha Momentum Fund (Paper) Balance: 25.4 USD`
  5. **Technical Explanation to Give**: This demonstrates that the frontend is actively connected to the AWS backend database and the live mock trading engine without exposing any live financial keys.

---

### B. The "Alert Playground" Tab (External Signal Simulation)
- **Menu Label**: `Alert Playground` (`data-tab="playground-tab"`, URL hash: `#playground`)
- **What it Displays**:
  - The TradingView Webhook Playground interface designed for ingesting external synthetic alerts.
  - Left panel: Alert Signal Generator with input fields:
    - **Ticker / Symbol**: Dropdown (`ETHUSD.P`, `BTCUSD.P`, `SOLUSD.P`).
    - **Action**: Dropdown (`BUY`, `SELL`, `CLOSE LONG`, `CLOSE SHORT`).
    - **Strategy Name (Optional)**: e.g., `Breakout Strategy`.
    - **Override Account Sizing (Custom Qty)**: Toggle switch (keep OFF).
    - **Execute Live Order**: Red toggle switch (strictly keep **OFF** to guarantee simulation mode).
  - Right panel:
    - **Webhook Payload JSON** box showing generated JSON.
    - **Simulation Logs Console** (`#sandbox-console`) for real-time output.
- **Actions to Perform on Video**:
  1. Click the `Alert Playground` tab in the top navigation.
  2. Confirm that **Ticker** is set to `ETHUSD.P (Ether Perpetual)` and **Action** is set to `BUY`.
  3. Notice the Webhook Payload box updates automatically:
     ```json
     {
       "ticker": "ETHUSD.P",
       "action": "buy",
       "passphrase": "my_secure_trading_passphrase_123"
     }
     ```
  4. Click the primary button: **`Run Simulation`** (`#trigger-sandbox-btn`).
  5. The button transitions to *"Running simulation..."* for approximately 0.5 seconds.
  6. The black console window (`#sandbox-console`) updates with the live execution output:
     ```
     [SUCCESS] Simulation complete.
     Ticker: ETHUSD.P
     Symbol Resolved: ETHUSD (Lot Size: 0.01)

     🟢 Account: Alpha Momentum Fund (Paper)
        Simulated successfully: Would place BUY market order of size 86266 lots (~862.6600 base asset) on ETHUSD @ mark price $2318.39. Sizing rule: Percentage Allocation = 80.0%. Leverage: 50x. Required margin: $39999.62 USD.

     🟢 Account: Delta Grid & Arbitrage (Paper)
        Simulated successfully: Would place BUY market order of size 25878 lots...

     🟢 Account: Institutional Swing Pool (Paper)
        Simulated successfully: Would place BUY market order of size 21 lots...

     🟢 Account: Retail Algorithmic Vault (Paper)
        Simulated successfully: Would place BUY market order of size 37739 lots...
     ```
  7. **Technical Explanation to Give**: This demonstrates that the AWS-hosted backend ingests webhooks, pulls live market mark prices from Delta Exchange, computes mathematical position sizing per vault, and validates risk constraints deterministically in under 300 milliseconds.

---

### C. The "Trades & PnL" Tab (Portfolio Position Tracking)
- **Menu Label**: `Trades & PnL` (`data-tab="pnl-tab"`, URL hash: `#pnl`)
- **What it Displays**:
  - **Live Open Positions Table**:
    - Columns: Account, Ticker, Side, Size, Entry Price, Mark Price, Margin, Leverage, Unrealized PnL.
    - Currently tracking live paper positions in `ETHUSD`, `BTCUSD`, and `SOLUSD`.
  - **Closed Position History Table**:
    - Columns: Closed Time, Account, Ticker, Side, Closed Size, Entry Price, Exit Price, Gross PnL, Fees, Net PnL.
    - Export Buttons: **`Export Trade Journal (Excel)`** and **`Export Local Signals (Excel)`**.
- **Actions to Perform on Video**:
  1. Click `Trades & PnL` in the top navigation.
  2. Point out the active Long position on `ETHUSD` for *Alpha Momentum Fund* showing real-time Mark Price updates.
  3. Scroll down slightly to display the closed position history proving historical trading activity with positive net realized PnL.

---

### D. The "Performance Analytics" Tab (Quantitative Metrics)
- **Menu Label**: `Performance Analytics` (`data-tab="analytics-tab"`, URL hash: `#analytics`)
- **What it Displays**:
  - Six Top KPI Metric Cards:
    - **Net Profit**: `$908.70 USD`
    - **Win Rate**: `75.0%`
    - **Profit Factor**: `7.71`
    - **Sharpe Ratio**: `3.30`
    - **Recovery Factor**: `72.49`
    - **Total Trades**: `12`
  - Two ApexCharts Interactive Graphs:
    - **Cumulative Portfolio Equity Curve** (upward-sloping equity growth).
    - **Historical Peak Drawdowns (%)** (shallow drawdowns strictly controlled under 13%).
  - One Heatmap:
    - **Time-of-Day Profitability Heatmap (Net PnL)** (visualizing trade profitability by hour and day of week).
- **Actions to Perform on Video**:
  1. Click `Performance Analytics` in the top navigation.
  2. Hover your mouse briefly over the **Sharpe Ratio (3.30)** and **Win Rate (75.0%)** KPI cards.
  3. Hover your mouse over one of the data points on the **Cumulative Portfolio Equity Curve** to show the ApexCharts interactive tooltip.
  4. **Technical Explanation to Give**: These quantitative metrics validate the algorithmic risk models (Wilder's ATR volatility stops and ZLSMA trend-following exits) executing automatically on the AWS backend.

---

### E. The "Global Settings" Tab (System Configuration)
- **Menu Label**: `Global Settings` (`data-tab="settings-tab"`, URL hash: `#settings`)
- **What it Displays**:
  - **Webhook Security Configuration**: Passphrase input (`my_secure_trading_passphrase_123`).
  - **Local Bot Dry Run Mode**: Toggle set to `True` (paper-trading enforcement).
  - **Notification Channels**: Discord / Telegram webhook URLs.
- **Actions to Perform on Video**:
  1. Click `Global Settings` to show the global security passphrase and safe dry-run state.
  2. Use this screen as the transition point into the **AWS Cloud Architecture** explanation before switching to the AWS Console.

---

## 3. Strict Safety Protocol During Demonstration
- **Zero Real-Money Risk**: Under no circumstances should the *"Execute Live Order"* switch in the Alert Playground be toggled to ON.
- **Always Keep Dry-Run Active**: All tests in the video must use the built-in sandbox or pre-seeded paper accounts.
- **Hide Personal Passwords**: The passphrase field is masked by default (`••••••••`); do not click "reveal" or expose sensitive secrets during recording.
