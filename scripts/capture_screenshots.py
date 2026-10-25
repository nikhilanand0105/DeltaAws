import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

OUT_DIR = os.path.abspath("docs/quantlens-final-report/figures")
os.makedirs(OUT_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1440,1200")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 1200)

try:
    print("[1/5] Loading QuantLens app at http://127.0.0.1:5001/quantlens ...")
    driver.get("http://127.0.0.1:5001/quantlens")
    time.sleep(2)

    # 1. Decision trace screenshot
    print("[2/5] Selecting Preset 1 and running compileStrategy()...")
    driver.execute_script("setPreset(1);")
    time.sleep(0.5)
    driver.execute_script("compileStrategy();")
    
    # Wait for compile to finish (poll for llmLatencyBadge visibility)
    for _ in range(15):
        time.sleep(1)
        visible = driver.execute_script("return document.getElementById('llmLatencyBadge').style.display !== 'none';")
        if visible:
            break

    time.sleep(1)
    # Scroll so decision trace & AI advisory are nicely framed
    driver.execute_script("window.scrollTo(0, 320);")
    time.sleep(1)
    p2 = os.path.join(OUT_DIR, "02_decision_trace.png")
    driver.save_screenshot(p2)
    print(f"  ✓ Saved {p2} ({os.path.getsize(p2)} bytes)")

    # 2. Backtest candlestick screenshot
    print("[3/5] Running Backtest for Candlestick & Trade Ledger...")
    driver.execute_script("window.scrollTo(0, 0); acceptAndBacktest();")
    time.sleep(3)
    # Scroll slightly down so candlestick and indicators are centered
    driver.execute_script("window.scrollTo(0, 120);")
    time.sleep(1)
    p3 = os.path.join(OUT_DIR, "03_backtest_candlestick.png")
    driver.save_screenshot(p3)
    print(f"  ✓ Saved {p3} ({os.path.getsize(p3)} bytes)")

    # 3. XAI Explainability tab
    print("[4/5] Loading XAI Explainability Tab...")
    driver.execute_script("window.scrollTo(0, 0); switchTab('tab-xai');")
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(1)
    p4 = os.path.join(OUT_DIR, "04_xai_explainability.png")
    driver.save_screenshot(p4)
    print(f"  ✓ Saved {p4} ({os.path.getsize(p4)} bytes)")

    # 4. Paper Broker tab
    print("[5/5] Loading Paper Broker Tab...")
    driver.execute_script("window.scrollTo(0, 0); switchTab('tab-broker');")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(1)
    p5 = os.path.join(OUT_DIR, "05_paper_broker.png")
    driver.save_screenshot(p5)
    print(f"  ✓ Saved {p5} ({os.path.getsize(p5)} bytes)")

finally:
    driver.quit()
    print("All UI screenshots captured successfully.")
