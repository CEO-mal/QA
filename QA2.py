from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Настройка Firefox
options = Options()
driver = webdriver.Firefox(options=options)

try:
    # Шаг 1: Открываем сайт
    driver.get("https://itcareerhub.de/ru")
    time.sleep(3)

    # Шаг 2: Находим раздел "Способы оплаты"
    payment_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Способы оплаты')]"))
    )

    # Прокручиваем к секции
    driver.execute_script("arguments[0].scrollIntoView();", payment_section)
    time.sleep(2)

    # Шаг 3: Делаем скриншот
    driver.save_screenshot("payment_section.png")
    print("Скриншот сохранён: payment_section.png")

finally:
    driver.quit()