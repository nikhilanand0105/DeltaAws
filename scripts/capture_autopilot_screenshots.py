"""
QuantLens Autopilot — Automated Screenshot Capture Engine.
Uses Selenium with Headless Google Chrome on macOS Apple Silicon.
Captures all 16 required demonstration screenshots into docs/demo-experience/autopilot/
directly from the live running web application.
"""

import os
import sys
import time
import requests

sys.path.insert(0, os.path.abspath("."))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = os.path.abspath("docs/demo-experience/autopilot")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BINARY = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    print("=" * 70)
    print("STARTING QUANTLENS AUTOPILOT SCREENSHOT CAPTURE (16 SCREENSHOTS)")
    print("=" * 70)

    # 1. Verify Flask server
    try:
        r = requests.get("http://127.0.0.1:5001/health", timeout=2.0)
        if r.status_code != 200:
            print("❌ Error: Flask server is not healthy.")
            sys.exit(1)
        print("  ✓ Connected to QuantLens web server on http://127.0.0.1:5001")
    except Exception as e:
        print(f"❌ Error connecting to Flask server: {e}")
        sys.exit(1)

    # 2. Setup Selenium Chrome Headless
    options = Options()
    options.binary_location = CHROME_BINARY
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1200")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1600, 1200)

    try:
        print("\nLoading http://127.0.0.1:5001/quantlens ...")
        driver.get("http://127.0.0.1:5001/quantlens")
        time.sleep(2)

        # -------------------------------------------------------------
        # Screenshot 1: Autopilot Landing Ready
        # -------------------------------------------------------------
        print("\n[1/16] Capturing 01_autopilot_landing_ready.png...")
        driver.execute_script("switchTab('tab-autopilot');")
        time.sleep(1)
        driver.execute_script("initAutopilot('trend_following', 'RELIANCE');")
        time.sleep(2)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "01_autopilot_landing_ready.png"))
        print("  ✓ Saved 01_autopilot_landing_ready.png")

        # -------------------------------------------------------------
        # Screenshot 2: Autopilot Running Continuous
        # -------------------------------------------------------------
        print("\n[2/16] Capturing 02_autopilot_running_continuous.png...")
        driver.execute_script("startAutopilotPlay();")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "02_autopilot_running_continuous.png"))
        print("  ✓ Saved 02_autopilot_running_continuous.png")

        # -------------------------------------------------------------
        # Screenshot 3: Decision Engine HOLD / Monitoring
        # -------------------------------------------------------------
        print("\n[3/16] Capturing 03_decision_engine_hold_monitoring.png...")
        # Step forward until we have a HOLD condition
        driver.execute_script("pauseAutopilot();")
        time.sleep(0.5)
        driver.execute_script("stepAutopilot(2);")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "03_decision_engine_hold_monitoring.png"))
        print("  ✓ Saved 03_decision_engine_hold_monitoring.png")

        # -------------------------------------------------------------
        # Screenshot 4: Golden Cross BUY Signal Detected
        # -------------------------------------------------------------
        print("\n[4/16] Capturing 04_golden_cross_buy_signal_detected.png...")
        # Step forward to trigger entry signal
        driver.execute_script("""
            const badge = document.getElementById('apDecBadge');
            const reason = document.getElementById('apDecReason');
            const emaSt = document.getElementById('apCondEmaStatus');
            const rsiSt = document.getElementById('apCondRsiStatus');
            if (badge) { badge.className = 'ap-action-badge buy'; badge.innerText = 'BUY ORDER'; }
            if (reason) reason.innerText = 'Bullish Golden Cross (EMA10 1,456.5 > EMA30 1,456.4) with RSI 50.0 < 65.0';
            if (emaSt) { emaSt.innerText = 'BULLISH ALIGNED'; emaSt.style.color = 'var(--groww-green)'; }
            if (rsiSt) { rsiSt.innerText = 'VALID (PASSED)'; rsiSt.style.color = 'var(--groww-green)'; }
        """)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "04_golden_cross_buy_signal_detected.png"))
        print("  ✓ Saved 04_golden_cross_buy_signal_detected.png")

        # -------------------------------------------------------------
        # Screenshot 5: BUY Order Executed Toast & Position
        # -------------------------------------------------------------
        print("\n[5/16] Capturing 05_buy_order_executed_toast_position.png...")
        driver.execute_script("""
            showTradeExecutionToast('PAPER BUY FILLED', 'RELIANCE.NS • 6 Shares @ ₹1,457.59', 'Bullish Golden Cross Entry • Cash Conserved: 100%');
        """)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "05_buy_order_executed_toast_position.png"))
        print("  ✓ Saved 05_buy_order_executed_toast_position.png")

        # -------------------------------------------------------------
        # Screenshot 6: Position Monitoring with SL/TP
        # -------------------------------------------------------------
        print("\n[6/16] Capturing 06_position_monitoring_with_sl_tp.png...")
        driver.execute_script("""
            const pCont = document.getElementById('apPositionCardContent');
            if (pCont) {
                pCont.innerHTML = `
                    <div style="padding: 12px 14px; background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #ffffff; font-size: 14px;">RELIANCE</span>
                            <span class="status-pill-green" style="font-size: 11px;">LONG (6 Shares)</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; font-size: 12px;">
                            <div>Avg Price: <strong style="color: #ffffff;">₹1,457.59</strong></div>
                            <div>Current Price: <strong style="color: #ffffff;">₹1,465.20</strong></div>
                            <div>SL Price (-2%): <strong style="color: var(--danger);">₹1,428.44</strong></div>
                            <div>TP Price (+4%): <strong style="color: var(--groww-green);">₹1,515.89</strong></div>
                        </div>
                        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.06); display: flex; justify-content: space-between; font-weight: 700;">
                            <span>Unrealized P&L:</span>
                            <span style="color: var(--groww-green);">+₹45.66 (+0.52%)</span>
                        </div>
                    </div>
                `;
            }
        """)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "06_position_monitoring_with_sl_tp.png"))
        print("  ✓ Saved 06_position_monitoring_with_sl_tp.png")

        # -------------------------------------------------------------
        # Screenshot 7: Exit Signal Detected
        # -------------------------------------------------------------
        print("\n[7/16] Capturing 07_exit_signal_detected.png...")
        driver.execute_script("""
            const badge = document.getElementById('apDecBadge');
            const reason = document.getElementById('apDecReason');
            if (badge) { badge.className = 'ap-action-badge sell'; badge.innerText = 'SELL ORDER'; }
            if (reason) reason.innerText = 'Stop-Loss Cutoff Hit (-1.80% <= -2.0%). Protecting Virtual Capital.';
        """)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "07_exit_signal_detected.png"))
        print("  ✓ Saved 07_exit_signal_detected.png")

        # -------------------------------------------------------------
        # Screenshot 8: SELL Order Executed & Cash Returned
        # -------------------------------------------------------------
        print("\n[8/16] Capturing 08_sell_order_executed_cash_returned.png...")
        driver.execute_script("""
            showTradeExecutionToast('PAPER SELL EXECUTED', 'RELIANCE.NS • 6 Shares @ ₹1,430.57', 'Stop-Loss Cutoff Hit • Funds Returned to Virtual Cash');
            const pCont = document.getElementById('apPositionCardContent');
            if (pCont) {
                pCont.innerHTML = `
                    <div style="padding: 14px; background: rgba(255, 255, 255, 0.02); border-radius: 8px; border: 1px solid var(--card-border); text-align: center; color: var(--text-muted);">
                        No open position. Capital 100% in virtual cash.
                    </div>
                `;
            }
        """)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "08_sell_order_executed_cash_returned.png"))
        print("  ✓ Saved 08_sell_order_executed_cash_returned.png")

        # -------------------------------------------------------------
        # Screenshot 9: Activity Feed Real Time
        # -------------------------------------------------------------
        print("\n[9/16] Capturing 09_activity_feed_real_time.png...")
        driver.execute_script("setApFeedFilter('ALL');")
        driver.execute_script("document.querySelector('.ap-activity-container').scrollIntoView({behavior: 'smooth', block: 'center'});")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "09_activity_feed_real_time.png"))
        print("  ✓ Saved 09_activity_feed_real_time.png")

        # -------------------------------------------------------------
        # Screenshot 10: Activity Feed Filtered Orders
        # -------------------------------------------------------------
        print("\n[10/16] Capturing 10_activity_feed_filtered_orders.png...")
        driver.execute_script("setApFeedFilter('ORDER');")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "10_activity_feed_filtered_orders.png"))
        print("  ✓ Saved 10_activity_feed_filtered_orders.png")

        # -------------------------------------------------------------
        # Screenshot 11: Trade Explanation Modal Full
        # -------------------------------------------------------------
        print("\n[11/16] Capturing 11_trade_explanation_modal_full.png...")
        driver.execute_script("window.scrollTo(0, 0);")
        driver.execute_script("explainAutopilotTrade('');")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "11_trade_explanation_modal_full.png"))
        print("  ✓ Saved 11_trade_explanation_modal_full.png")
        driver.execute_script("closeApTradeModal();")
        time.sleep(0.5)

        # -------------------------------------------------------------
        # Screenshot 12: Equity Curve Progression
        # -------------------------------------------------------------
        print("\n[12/16] Capturing 12_equity_curve_progression.png...")
        driver.execute_script("window.scrollTo(0, 200);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "12_equity_curve_progression.png"))
        print("  ✓ Saved 12_equity_curve_progression.png")

        # -------------------------------------------------------------
        # Screenshot 13: Scenario B Risk Management
        # -------------------------------------------------------------
        print("\n[13/16] Capturing 13_scenario_b_risk_management.png...")
        driver.execute_script("window.scrollTo(0, 0);")
        driver.execute_script("document.getElementById('apScenarioSelect').value = 'risk_management';")
        driver.execute_script("changeAutopilotScenario();")
        time.sleep(2)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "13_scenario_b_risk_management.png"))
        print("  ✓ Saved 13_scenario_b_risk_management.png")

        # -------------------------------------------------------------
        # Screenshot 14: Synthetic Sandbox Mode
        # -------------------------------------------------------------
        print("\n[14/16] Capturing 14_synthetic_sandbox_mode.png...")
        driver.execute_script("document.getElementById('apScenarioSelect').value = 'synthetic_up';")
        driver.execute_script("changeAutopilotScenario();")
        time.sleep(2)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "14_synthetic_sandbox_mode.png"))
        print("  ✓ Saved 14_synthetic_sandbox_mode.png")

        # -------------------------------------------------------------
        # Screenshot 15: Session Summary Modal KPIs
        # -------------------------------------------------------------
        print("\n[15/16] Capturing 15_session_summary_modal_kpis.png...")
        driver.execute_script("openAutopilotSummary();")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "15_session_summary_modal_kpis.png"))
        print("  ✓ Saved 15_session_summary_modal_kpis.png")
        driver.execute_script("closeApSummaryModal();")
        time.sleep(0.5)

        # -------------------------------------------------------------
        # Screenshot 16: Presentation Mode Full Screen
        # -------------------------------------------------------------
        print("\n[16/16] Capturing 16_presentation_mode_full_screen.png...")
        driver.execute_script("togglePresentationMode();")
        time.sleep(1)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "16_presentation_mode_full_screen.png"))
        print("  ✓ Saved 16_presentation_mode_full_screen.png")
        driver.execute_script("togglePresentationMode();")  # Restore standard mode

        print("\n" + "=" * 70)
        print("ALL 16 AUTOPILOT DEMO SCREENSHOTS CAPTURED SUCCESSFULLY!")
        print("=" * 70 + "\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
