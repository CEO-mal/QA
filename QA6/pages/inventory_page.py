from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    @staticmethod
    def _add_button(product_name):
        # "Sauce Labs Bolt T-Shirt" -> "add-to-cart-sauce-labs-bolt-t-shirt"
        product_id = product_name.lower().replace(" ", "-")
        return By.ID, f"add-to-cart-{product_id}"

    def add_to_cart(self, product_name):
        self.click(self._add_button(product_name))

    def go_to_cart(self):
        self.click(self.CART_LINK)
