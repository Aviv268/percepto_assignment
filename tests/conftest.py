import pytest
import logging
import json
import os
import random
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def setup_logger():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    logs_dir = os.path.join(project_root, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, f"test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    return logger


logger = setup_logger()


@pytest.fixture(scope='session')
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=en")
    drv = webdriver.Chrome(options=chrome_options)
    yield drv
    drv.quit()


@pytest.fixture(scope='session')
def user_data():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(project_root, 'data', 'user_details.json')

    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['users']


@pytest.fixture
def random_user(user_data):
    return random.choice(user_data)


def pytest_exception_interact(node, call, report):
    """Attach screenshot to Allure on test failures."""
    if report.failed:
        driver_fixture = node.funcargs.get("driver", None)
        if driver_fixture:
            screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            screenshot_path = os.path.join(screenshot_dir, f"{node.name}_fail.png")
            try:
                driver_fixture.save_screenshot(screenshot_path)
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"{node.name}_fail_screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
            except WebDriverException as e:
                logging.error(f"Could not take screenshot: {e}")
