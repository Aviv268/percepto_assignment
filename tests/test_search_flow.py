import pytest
import allure
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.home_page import HomePage


@allure.title("TerminalX Automated Test")
@pytest.mark.usefixtures("driver")
class TestTerminalX:
    def test_terminalx_scenario(self, driver, random_user):
        home_page = HomePage(driver)
        home_page.navigate_to_home_page()

        login_page = home_page.click_login_link()
        login_page.login(random_user['username'], random_user['password'])

        home_page.enter_search_phrase("hello")
        search_page = SearchResultsPage(driver)
        search_page.verify_dropdown_results("hello kitty")
        search_page.verify_products_sorted_by_price()
        search_page.click_third_product()
        product_page = ProductPage(driver)
        product_page.verify_price_and_font_size()
