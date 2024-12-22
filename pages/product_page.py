import allure
import pytest_check as check
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    PRICE_LABEL = (By.CSS_SELECTOR, '[data-test-id="qa-pdp-price-final"]')
    DREAM_CARD_POP_UP = (By.CSS_SELECTOR, '.btn_2OAI.btn-refuse_3lZA')  # Adjust if needed

    @allure.step("Verify product price is displayed and font size is 1.8rem (soft assert).")
    def verify_price_and_font_size(self):
        if self.is_visible(self.DREAM_CARD_POP_UP):
            self.click(self.DREAM_CARD_POP_UP)

        price_el = self.wait_for_element_visible(self.PRICE_LABEL)
        price_text = price_el.text.strip()
        check.is_true(
            price_text,
            "Price is not displayed."
        )

        font_size = price_el.value_of_css_property("font-size")
        check.equal(
            font_size,
            "1.8rem",
            f"Expected font-size 1.8rem but got '{font_size}'."
        )
