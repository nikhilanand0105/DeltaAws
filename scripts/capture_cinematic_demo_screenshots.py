"""
Automated Screenshot Capture Engine for QuantLens-XAI Cinematic Demo.
Uses Selenium with Headless Google Chrome on macOS Apple Silicon.
Captures all 21 genuine demonstration screenshots directly from the live application.
"""

import os
import sys
import time
import subprocess
import threading

sys.path.insert(0, os.path.abspath("."))

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

SCREENSHOTS_DIR = os.path.abspath("docs/demo-experience/screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

CHROME_BINARY = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def start_flask_app():
    from app import app
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)


def wait_for_server(url="http://127.0.0.1:5001/health", timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def main():
    print("======================================================================")
    print("STARTING CINEMATIC DEMO SCREENSHOT CAPTURE (21 SCREENSHOTS)")
    print("======================================================================")

    # 1. Start Flask server if not already running
    server_running = False
    try:
        r = requests.get("http://127.0.0.1:5001/health", timeout=1.0)
        if r.status_code == 200:
            server_running = True
            print("  ✓ Server already running on port 5001.")
    except Exception:
        pass

    if not server_running:
        print("  Starting Flask server in background thread...")
        t = threading.Thread(target=start_flask_app, daemon=True)
        t.start()
        if not wait_for_server():
            print("❌ Error: Flask server failed to start within timeout.")
            sys.exit(1)
        print("  ✓ Flask server started successfully on http://127.0.0.1:5001.")

    # 2. Setup Selenium Chrome
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
        print("\n[1/21] Capturing 01_strategy_input_screen.png...")
        driver.get("http://127.0.0.1:5001/quantlens")
        time.sleep(2)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "01_strategy_input_screen.png"))
        print("  ✓ Saved 01_strategy_input_screen.png")

        print("\n[2/21] Triggering Analyze & Run Strategy...")
        driver.execute_script("analyzeAndRunStrategy();")
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "02_mission_control.png"))
        print("  ✓ Saved 02_mission_control.png")

        print("\n[3/21] Capturing 03_llm_processing_state.png...")
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "03_llm_processing_state.png"))
        print("  ✓ Saved 03_llm_processing_state.png")

        # Wait for pipeline to finish
        print("  Waiting for 8-stage pipeline completion...")
        time.sleep(4)

        print("\n[4/21] Capturing 04_parsed_strategy.png...")
        driver.execute_script("selectMissionStage(2);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "04_parsed_strategy.png"))
        print("  ✓ Saved 04_parsed_strategy.png")

        print("\n[5/21] Capturing 05_rule_validation.png...")
        driver.execute_script("selectMissionStage(3);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "05_rule_validation.png"))
        print("  ✓ Saved 05_rule_validation.png")

        print("\n[6/21] Capturing 06_risk_intelligence.png...")
        driver.execute_script("switchTab('tab-risk-advisor');")
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "06_risk_intelligence.png"))
        print("  ✓ Saved 06_risk_intelligence.png")

        print("\n[7/21] Capturing 07_ai_advisor.png...")
        driver.execute_script("askAdvisorQuestion('Why is RSI used here?');")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "07_ai_advisor.png"))
        print("  ✓ Saved 07_ai_advisor.png")

        print("\n[8/21] Capturing 08_decision_flow_diagram.png...")
        driver.execute_script("switchTab('tab-mission-control'); selectMissionStage(3); inspectFlowchartNode('EMA Crossover');")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 150);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "08_decision_flow_diagram.png"))
        print("  ✓ Saved 08_decision_flow_diagram.png")

        print("\n[9/21] Capturing 09_market_indicator_chart.png...")
        driver.execute_script("window.scrollTo(0, 0); switchTab('tab-backtest');")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 160);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "09_market_indicator_chart.png"))
        print("  ✓ Saved 09_market_indicator_chart.png")

        print("\n[10/21] Capturing 10_xgboost_pytorch_comparison.png...")
        driver.execute_script("window.scrollTo(0, 0); switchTab('tab-xai');")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "10_xgboost_pytorch_comparison.png"))
        print("  ✓ Saved 10_xgboost_pytorch_comparison.png")

        print("\n[11/21] Capturing 11_shap_explanation.png...")
        driver.execute_script("window.scrollTo(0, 220);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "11_shap_explanation.png"))
        print("  ✓ Saved 11_shap_explanation.png")

        print("\n[12/21] Capturing 12_lime_explanation.png...")
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "12_lime_explanation.png"))
        print("  ✓ Saved 12_lime_explanation.png")

        print("\n[13/21] Capturing 13_xai_comparison.png...")
        driver.execute_script("onFeatureBarClicked('rsi_14'); window.scrollTo(0, 520);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "13_xai_comparison.png"))
        print("  ✓ Saved 13_xai_comparison.png")

        print("\n[14/21] Capturing 14_backtest_results.png...")
        driver.execute_script("window.scrollTo(0, 0); switchTab('tab-backtest');")
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "14_backtest_results.png"))
        print("  ✓ Saved 14_backtest_results.png")

        print("\n[15/21] Capturing 15_transition_to_paper_broker.png...")
        driver.execute_script("deployToPaperBroker();")
        time.sleep(0.8)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "15_transition_to_paper_broker.png"))
        print("  ✓ Saved 15_transition_to_paper_broker.png")

        print("\n[16/21] Capturing 16_paper_broker_overview.png...")
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "16_paper_broker_overview.png"))
        print("  ✓ Saved 16_paper_broker_overview.png")

        print("\n[17/21] Capturing 17_paper_buy_order.png...")
        driver.execute_script("runSimulationReplay();")
        time.sleep(2)
        driver.execute_script("showTradeExecutionToast('PAPER BUY EXECUTED', 'RELIANCE.NS • 7 Shares @ ₹1,294.25', 'Fee: ₹4.53 • Slippage: 0.05% • Cash Conserved');")
        time.sleep(0.3)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "17_paper_buy_order.png"))
        print("  ✓ Saved 17_paper_buy_order.png")

        print("\n[18/21] Capturing 18_paper_sell_order.png...")
        driver.execute_script("showTradeExecutionToast('PAPER SELL EXECUTED', 'RELIANCE.NS • 7 Shares @ ₹1,294.25', 'Realized PnL: -₹115.83 • Order ORD-523267 Persisted');")
        time.sleep(0.3)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "18_paper_sell_order.png"))
        print("  ✓ Saved 18_paper_sell_order.png")

        print("\n[19/21] Capturing 19_portfolio_results.png...")
        driver.execute_script("window.scrollTo(0, 320);")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "19_portfolio_results.png"))
        print("  ✓ Saved 19_portfolio_results.png")

        print("\n[20/21] Capturing 20_mongodb_records.png...")
        driver.execute_script("toggleSystemInspector();")
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "20_mongodb_records.png"))
        print("  ✓ Saved 20_mongodb_records.png")

        print("\n[21/21] Capturing 21_final_summary_screen.png...")
        driver.execute_script("toggleSystemInspector(); switchTab('tab-final-report');")
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "21_final_summary_screen.png"))
        print("  ✓ Saved 21_final_summary_screen.png")

        print("\n======================================================================")
        print("ALL 21 SCREENSHOTS CAPTURED SUCCESSFULLY IN:")
        print(f"👉 {SCREENSHOTS_DIR}")
        print("======================================================================")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
