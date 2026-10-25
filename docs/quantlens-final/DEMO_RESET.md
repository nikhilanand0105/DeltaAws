# QuantLens-XAI: Safe Demo Reset Procedure & State Restoration

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand

---

## 1. Reset Principles

To ensure clean demonstrations across repeated viva evaluation sessions:
1. **Safety First**: The reset procedure affects **ONLY** the seeded virtual paper account (`data/paper_broker_state.json`) and temporary simulation logs.
2. **Preserves Core Code & Artifacts**: Pretrained model weights (`models/`), cached datasets (`data/historical/`), and Git repository history are permanently preserved.
3. **Restores Initial Capital**: Returns the virtual cash balance to exactly **₹1,00,000.00 INR**.

---

## 2. One-Click Reset Script

Run the dedicated reset script:
```bash
./reset_quantlens_demo.sh
```

### What the script executes:
```bash
#!/usr/bin/env bash
echo "Resetting QuantLens Paper Broker virtual state..."
python3 -c "
from quantlens.paper_broker import get_paper_broker
broker = get_paper_broker()
broker.reset_account(initial_capital=100000.0)
print('QuantLens Paper Broker successfully reset to ₹1,00,000.00 virtual cash.')
"
```

---

## 3. UI-Based In-App Reset

During a live presentation, you can also reset directly from the web browser:
1. Navigate to **Tab 4: Paper Broker & Replay**.
2. Click the red button: **`🔄 Reset Virtual Funds to ₹1,00,000`**.
3. Confirm the browser prompt.
4. The dashboard will immediately refresh to:
   - **Total Portfolio Value:** ₹1,00,000.00
   - **Available Cash:** ₹1,00,000.00
   - **Invested Value:** ₹0.00
   - **Open Positions:** 0
   - **Unrealized P&L:** ₹0.00
   - **Audit Entry:** `AUD-0001 [ACCOUNT_RESET]: Paper broker reset to initial virtual capital of ₹1,00,000.00 INR`
