import logging
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "qa-login-email-input")
    PASSWORD_FIELD = (By.ID, "qa-login-password-input")
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test-id="qa-login-submit"]')
    LOADER = (By.CSS_SELECTOR, "img[src*='loader.gif']")

    def login(self, username, password):
        self.logger.info(f"Logging in with user: '{username}'")
        self.type_text(self.USERNAME_FIELD, username)
        self.type_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_element_invisible(self.LOADER, 5)
