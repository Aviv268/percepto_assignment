import allure
import pytest_check as check
from selenium.webdriver.common.by import By
from .base_page import BasePage
from .product_page import ProductPage


class SearchResultsPage(BasePage):
    SUGGESTIONS = (By.CSS_SELECTOR, "ul.list_3tWy li.element_1cy1")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "li.container_2pxt div.price_3AB9 .bold_2wBM")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "ul.list_3tWy li.container_2pxt > a")

    @allure.step("Verify suggestions contain '{expected_phrase}' (soft assert).")
    def verify_dropdown_results(self, expected_phrase):
        results = self.driver.find_elements(*self.SUGGESTIONS)
        for r in results:
            check.is_true(
                expected_phrase.lower() in r.text.strip().lower(),
                f"Suggestion '{r.text}' doesn't contain '{expected_phrase}'"
            )

    @allure.step("Verify products are sorted ascending by price (soft assert).")
    def verify_products_sorted_by_price(self):
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        prices = []
        for pe in price_elements:
            txt = pe.text.replace("₪", "").replace("$", "").strip()
            prices.append(float(txt))
        check.equal(
            prices,
            sorted(prices),
            "Products are not in ascending order by price."
        )

    @allure.step("Click the third product in the list.")
    def click_third_product(self):
        self.wait_for_element_visible(self.PRODUCT_ITEMS)
        items = self.driver.find_elements(*self.PRODUCT_ITEMS)
        if len(items) < 3:
            raise AssertionError("Fewer than 3 products found.")
        items[2].click()
        return ProductPage(self.driver)
