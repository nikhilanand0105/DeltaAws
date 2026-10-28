#!/usr/bin/env python3
"""
Captures high-resolution visual demonstration screenshots of QuantLens-XAI
across all primary screens, the continuous Autopilot cockpit, and the refined
Trade Explanation modal featuring the 3-concept separation and Rule Precedence notice.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5001/quantlens"
CHROMEDRIVER_PATH = "/Users/nikhilanand/.cache/selenium/chromedriver/mac-arm64/156.0.8078.47/chromedriver"
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "final-polish", "screenshots"))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def main():
    print(f"Starting QuantLens-XAI Screenshot Automation...")
    print(f"Target URL: {BASE_URL}")
    print(f"Output Directory: {SCREENSHOT_DIR}")

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1600,1050")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=opts)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(BASE_URL)
        time.sleep(3)
        print("Page loaded successfully.")

        # 1. Strategy Builder Tab
        print("[1/7] Capturing Strategy Builder...")
        driver.execute_script("if (typeof switchTab === 'function') switchTab('tab-builder');")
        time.sleep(1.5)
        path_01 = os.path.join(SCREENSHOT_DIR, "01_strategy_builder.png")
        driver.save_screenshot(path_01)
        print(f"  ✓ Saved {path_01} ({os.path.getsize(path_01)} bytes)")

        # 2. Mission Control Pipeline
        print("[2/7] Capturing Mission Control...")
        driver.execute_script("if (typeof switchTab === 'function') switchTab('tab-pipeline');")
        time.sleep(1.5)
        path_02 = os.path.join(SCREENSHOT_DIR, "02_mission_control.png")
        driver.save_screenshot(path_02)
        print(f"  ✓ Saved {path_02} ({os.path.getsize(path_02)} bytes)")

        # 3. Explainable AI Lab
        print("[3/7] Capturing Explainable AI Lab...")
        driver.execute_script("if (typeof switchTab === 'function') switchTab('tab-xai');")
        time.sleep(1.5)
        path_03 = os.path.join(SCREENSHOT_DIR, "03_xai_explainability.png")
        driver.save_screenshot(path_03)
        print(f"  ✓ Saved {path_03} ({os.path.getsize(path_03)} bytes)")

        # 4. Paper Broker Dashboard
        print("[4/7] Capturing Paper Broker Portfolio...")
        driver.execute_script("if (typeof switchTab === 'function') switchTab('tab-paper-broker');")
        time.sleep(1.5)
        path_04 = os.path.join(SCREENSHOT_DIR, "04_paper_broker_portfolio.png")
        driver.save_screenshot(path_04)
        print(f"  ✓ Saved {path_04} ({os.path.getsize(path_04)} bytes)")

        # 5. QuantLens Autopilot Cockpit
        print("[5/7] Initializing and Capturing Autopilot Cockpit...")
        driver.execute_script("if (typeof switchTab === 'function') switchTab('tab-autopilot');")
        time.sleep(1.0)
        # Prepare demo session if not already running
        driver.execute_script("if (typeof prepareAutopilot === 'function') prepareAutopilot();")
        time.sleep(2.5)

        # Step 15 bars so indicators and telemetry populate
        for _ in range(15):
            driver.execute_script("if (typeof stepAutopilot === 'function') stepAutopilot(1);")
            time.sleep(0.15)

        time.sleep(2.0)
        path_05 = os.path.join(SCREENSHOT_DIR, "05_autopilot_cockpit.png")
        driver.save_screenshot(path_05)
        print(f"  ✓ Saved {path_05} ({os.path.getsize(path_05)} bytes)")

        # 6. Trade Explanation Modal (with 3-Way Separation & Rule Precedence)
        print("[6/7] Triggering and Capturing Trade Explanation Modal...")
        # Step until at least 1 order exists
        order_found = False
        for _ in range(40):
            has_orders = driver.execute_script("""
                const list = document.getElementById('apOrdersList');
                return list && list.querySelectorAll('button').length > 0;
            """)
            if has_orders:
                order_found = True
                break
            driver.execute_script("if (typeof stepAutopilot === 'function') stepAutopilot(1);")
            time.sleep(0.1)

        time.sleep(1.0)
        # Click the first Explain button
        driver.execute_script("""
            const btns = document.querySelectorAll('#apOrdersList button');
            if (btns.length > 0) btns[0].click();
        """)
        time.sleep(2.0)
        path_06 = os.path.join(SCREENSHOT_DIR, "06_trade_explanation_modal.png")
        driver.save_screenshot(path_06)
        print(f"  ✓ Saved {path_06} ({os.path.getsize(path_06)} bytes)")

        # Close Trade Explanation Modal
        driver.execute_script("if (typeof closeApTradeModal === 'function') closeApTradeModal();")
        time.sleep(0.8)

        # 7. Session Summary Modal
        print("[7/7] Opening and Capturing Session Summary Modal...")
        driver.execute_script("if (typeof openAutopilotSummary === 'function') openAutopilotSummary();")
        time.sleep(2.0)
        path_07 = os.path.join(SCREENSHOT_DIR, "07_session_summary_modal.png")
        driver.save_screenshot(path_07)
        print(f"  ✓ Saved {path_07} ({os.path.getsize(path_07)} bytes)")

        print("\nAll 7 visual demonstration screenshots captured successfully!")

    except Exception as e:
        print(f"Error during screenshot capture: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
