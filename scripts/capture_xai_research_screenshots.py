"""
Captures high-resolution screenshots of Tab 09: XAI Research Lab for documentation.
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = "/Users/nikhilanand/.cache/selenium/chromedriver/mac-arm64/156.0.8078.47/chromedriver"
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "xai-research", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1200")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Navigating to QuantLens-XAI platform at http://127.0.0.1:5001/quantlens...")
    driver.get("http://127.0.0.1:5001/quantlens")
    time.sleep(2)

    # 1. Switch to Tab 09: XAI Research Lab
    print("Switching to Tab 09: XAI Research Lab...")
    driver.execute_script("switchTab('tab-xai-research');")
    time.sleep(3)

    # Screenshot 1: Overview & 3-Panel Closed-Loop Feedback
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "01_xai_closed_loop_feedback.png"))
    print("  ✓ Saved 01_xai_closed_loop_feedback.png")

    # Scroll down to Model C Grad-CAM & 10-Metric Suite
    driver.execute_script("window.scrollTo(0, 950);")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "02_xai_gradcam_and_10_metrics.png"))
    print("  ✓ Saved 02_xai_gradcam_and_10_metrics.png")

    # Scroll down to Sensitivity Analysis & Retraining Leaderboard
    driver.execute_script("window.scrollTo(0, 1850);")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "03_xai_sensitivity_and_retraining.png"))
    print("  ✓ Saved 03_xai_sensitivity_and_retraining.png")

    # Scroll down to Faculty Viva Defense Guide
    driver.execute_script("window.scrollTo(0, 2600);")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "04_xai_faculty_viva_guide.png"))
    print("  ✓ Saved 04_xai_faculty_viva_guide.png")

    print("\nAll 4 XAI Research Lab screenshots captured successfully!")

finally:
    driver.quit()
