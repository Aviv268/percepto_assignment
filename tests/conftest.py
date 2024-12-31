import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def setup_logger():
    project_root = Path(__file__).resolve().parent.parent
    logs_dir = project_root / 'logs'
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / f"test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    return logging.getLogger()


setup_logger()


@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def user_data():
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / 'data' / 'user_details.json'

    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['users']


@pytest.fixture
def random_user(user_data):
    return random.choice(user_data)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}_fail.png"
            os.makedirs("screenshots", exist_ok=True)
            try:
                driver.save_screenshot(screenshot_path)
                with open(screenshot_path, "rb") as f:
                    allure.attach(f.read(), name=f"{item.name}_fail_screenshot", attachment_type=allure.attachment_type.PNG)
            except WebDriverException as e:
                print(f"Could not take screenshot: {e}")
