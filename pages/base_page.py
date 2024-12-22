import logging
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def wait_for_element_visible(self, locator, timeout=10):
        self.logger.debug(f"Waiting for element {locator} to be visible.")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not visible after {timeout}s"
        )

    def wait_for_element_invisible(self, locator, timeout=10):
        self.logger.debug(f"Waiting for element {locator} to be invisible.")
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator),
            message=f"Element {locator} did not become invisible within {timeout} seconds"
        )

    def wait_for_element_clickable(self, locator, timeout=10):
        self.logger.debug(f"Waiting for element {locator} to be clickable.")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Element {locator} not clickable after {timeout}s"
        )

    def click(self, locator, timeout=10):
        el = self.wait_for_element_clickable(locator, timeout)
        self.logger.debug(f"Clicking on element {locator}.")
        el.click()

    def type_text(self, locator, text, timeout=10):
        el = self.wait_for_element_visible(locator, timeout)
        el.clear()
        self.logger.debug(f"Typing '{text}' into element {locator}.")
        el.send_keys(text)

    def is_visible(self, locator, timeout=5):
        self.logger.debug(f"Checking visibility of {locator} for up to {timeout}s.")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def take_screenshot(self, name="screenshot"):
        screenshot_path = f'./tests/screenshots/{name}.png'
        self.driver.save_screenshot(screenshot_path)
        allure.attach.file(
            screenshot_path,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
