import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_text_in_iframe(driver):
    """Задание 1: Проверка наличия текста в iframe."""
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")

    # Найти iframe с текстом и переключиться в него
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "my-iframe"))
    )

    # Найти элемент с искомым текстом
    expected = "semper posuere integer et senectus justo curabitur."
    paragraph = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//p[contains(normalize-space(.), '{expected}')]")
        )
    )

    # Убедиться, что текст отображается
    assert paragraph.is_displayed()
    assert expected in paragraph.text

    driver.switch_to.default_content()


def close_consent_popup(driver):
    """Закрывает окно согласия на cookies, если оно появилось."""
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".fc-cta-do-not-consent, .fc-cta-consent")
            )
        )
        button.click()
    except TimeoutException:
        pass


def test_drag_photo_to_trash(driver):
    """Задание 2: Перетаскивание первой фотографии в корзину."""
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
    close_consent_popup(driver)

    # Демо Photo Manager находится внутри iframe
    frame = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "iframe.demo-frame[src*='photo-manager']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", frame)
    driver.switch_to.frame(frame)

    # Захватить первую фотографию и перетащить её в корзину
    first_photo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#gallery li:first-child"))
    )
    trash = driver.find_element(By.ID, "trash")
    ActionChains(driver).drag_and_drop(first_photo, trash).perform()

    # Дождаться, пока фотография появится в корзине
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#trash li")) == 1
    )

    trash_photos = driver.find_elements(By.CSS_SELECTOR, "#trash li")
    gallery_photos = driver.find_elements(By.CSS_SELECTOR, "#gallery li")

    assert len(trash_photos) == 1, "В корзине должна быть 1 фотография"
    assert len(gallery_photos) == 3, "В галерее должно остаться 3 фотографии"

    driver.switch_to.default_content()
