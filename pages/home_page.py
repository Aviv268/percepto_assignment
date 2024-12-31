from selenium.webdriver.common.by import By

from .base_page import BasePage
from .login_page import LoginPage
from .search_results_page import SearchResultsPage


class HomePage(BasePage):
    URL = "https://www.terminalx.com/"

    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test-id="qa-header-login-button"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-button_1ENs")
    SEARCH_BAR = (By.CSS_SELECTOR, '[data-test-id="qa-search-box-input"]')
    LOADER = (By.CSS_SELECTOR, "img[src*='loader.gif']")

    def navigate_to_home_page(self):
        self.logger.info("Navigating to TerminalX homepage")
        self.driver.get(self.URL)

    def click_login_link(self):
        self.logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        return LoginPage(self.driver)

    def enter_search_phrase(self, text):
        self.logger.info(f"Entering search text: {text}")
        self.wait_for_element_invisible(self.LOADER, 5)
        self.click(self.SEARCH_BUTTON)
        self.type_text(self.SEARCH_BAR, text)
        return SearchResultsPage(self.driver)
