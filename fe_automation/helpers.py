import os
import allure
import logging
from datetime import datetime


def capture_screenshot(page, test_name):
    screenshots_dir = 'reports/screenshots'
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    page.screenshot(path=screenshot_path)
    allure.attach.file(screenshot_path, name=f"Screenshot_{test_name}", attachment_type=allure.attachment_type.PNG)


def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/fe_automation.log'),
            logging.StreamHandler()
        ]
    )