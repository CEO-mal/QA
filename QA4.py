import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_button_text_changes(driver):
    """Задание 1: Проверка изменения текста кнопки."""
    driver.get("http://uitestingplayground.com/textinput")

    text_input = driver.find_element(By.ID, "newButtonName")
    text_input.clear()
    text_input.send_keys("ITCH")

    button = driver.find_element(By.ID, "updatingButton")  # синяя кнопка
    button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "updatingButton"), "ITCH")
    )
    assert button.text == "ITCH"


def test_third_image_alt(driver):
    """Задание 2: Проверка загрузки изображений."""
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

    # Все изображения загружены, когда появляется текст "Done!"
    WebDriverWait(driver, 30).until(
        EC.text_to_be_present_in_element((By.ID, "text"), "Done!")
    )

    images = driver.find_elements(By.CSS_SELECTOR, "#image-container img")
    alt = images[2].get_attribute("alt")

    assert alt == "award"