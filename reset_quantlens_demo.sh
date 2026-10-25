#!/usr/bin/env bash
# QuantLens-XAI: Safe Demo Reset Script
# Restores virtual paper funds to ₹1,00,000.00 and clears temporary simulation orders.
# Preserves code, model weights, and historical datasets.

set -e

echo "======================================================================"
echo "    QuantLens-XAI: Resetting Virtual Paper Account State"
echo "======================================================================"

python3 -c "
from quantlens.paper_broker import get_paper_broker
broker = get_paper_broker()
broker.reset_account(initial_capital=100000.0)
summary = broker.get_dashboard_summary()
print(f'  ✓ Paper Broker reset successfully.')
print(f'  ✓ Starting Cash: ₹{summary[\"available_cash\"]:,.2f} INR')
print(f'  ✓ Portfolio Equity: ₹{summary[\"total_portfolio_value\"]:,.2f} INR')
print(f'  ✓ Open Positions: {summary[\"open_positions_count\"]}')
print(f'  ✓ Mode: {summary[\"trading_mode\"]}')
"

echo "Demo reset complete. Ready for a new faculty demonstration."
