#!/usr/bin/env bash
# QuantLens-XAI: Safe Demo Reset Script
# Restores virtual paper funds to ₹10,00,000.00 (Groww-inspired baseline)
# and clears temporary simulation orders in MongoDB and SQLite.
# Preserves code, model weights, and historical datasets.

set -e

echo "======================================================================"
echo "    QuantLens-XAI: Resetting Virtual Paper Account State"
echo "    Database: MongoDB quantlens_xai (localhost:27017)"
echo "======================================================================"

python3 -c "
from quantlens.paper_broker import get_paper_broker
from quantlens.db_mongodb import get_mongodb_manager

broker = get_paper_broker()
broker.reset_account(initial_capital=1000000.0)
summary = broker.get_dashboard_summary()

mongo = get_mongodb_manager()
status = mongo.get_status() if mongo.is_connected() else {'connected': False}
collections = status.get('collections', {})

print(f'  ✓ Paper Broker reset successfully.')
print(f'  ✓ Starting Cash: ₹{summary[\"available_cash\"]:,.2f} INR')
print(f'  ✓ Portfolio Equity: ₹{summary[\"total_portfolio_value\"]:,.2f} INR')
print(f'  ✓ Open Positions: {summary[\"open_positions_count\"]}')
print(f'  ✓ Trading Mode: {summary[\"trading_mode\"]}')
print(f'  ✓ MongoDB Status: Connected={status.get(\"connected\")} | Collections: {collections}')
"

echo "Demo reset complete. Ready for a new faculty demonstration."
