from selenium import webdriver

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def create_driver():
    options = webdriver.ChromeOptions()
    # Отключаем менеджер паролей Chrome: его окно может перекрыть страницу
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def test_checkout_total():
    driver = create_driver()
    try:
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        for product in ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]:
            inventory_page.add_to_cart(product)
        inventory_page.go_to_cart()

        CartPage(driver).checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_form("Nadya", "Tester", "10115")
        total = checkout_page.get_total()
    finally:
        driver.quit()

    assert total == "$58.29"
