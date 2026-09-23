import re

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://itcareerhub.de/ru"

HEADER_LINKS = ["Программы", "Способы оплаты", "О нас", "Отзывы", "Блог"]


def close_cookie_banner(page: Page) -> None:
    """Закрываем баннер cookie, если он появился: он может перекрывать кнопки."""
    button = page.get_by_role("button", name=re.compile("Accept essential only", re.I))
    try:
        button.wait_for(state="visible", timeout=5000)
        button.click()
    except Exception:
        pass  # баннера нет — ничего не делаем


def header(page: Page):
    """Шапка сайта — блок, в котором находится логотип ITCareerHub."""
    return page.locator("[id^=rec]").filter(
        has=page.locator('img[alt="IT Career Hub"]')
    ).first


def open_contacts_link(page: Page):
    """Открываем выпадающее меню «О нас» и возвращаем пункт «Контакты»."""
    about = header(page).get_by_role("link", name="О нас", exact=True)
    contacts = page.locator('a[href*="contact-us"]').filter(visible=True).first
    about.hover()
    try:
        contacts.wait_for(state="visible", timeout=3000)
    except Exception:
        about.click()  # если меню не открылось по наведению — открываем кликом
    return contacts


@pytest.fixture
def home(page: Page) -> Page:
    page.goto(BASE_URL)
    close_cookie_banner(page)
    return page


def test_header_elements_are_visible(home: Page):
    top = header(home)

    # Логотип
    expect(top.locator('img[alt="IT Career Hub"]')).to_be_visible()

    # Ссылки меню
    for name in HEADER_LINKS:
        expect(top.get_by_role("link", name=name, exact=True)).to_be_visible()

    # «Контакты» находится в выпадающем меню «О нас»
    contacts = open_contacts_link(home)
    expect(contacts).to_be_visible()
    expect(contacts).to_have_text("Контакты")

    # Переключатели языка
    expect(top.get_by_role("link", name="ru", exact=True)).to_be_visible()
    expect(top.get_by_role("link", name="de", exact=True)).to_be_visible()


def test_callback_popup(home: Page):
    # 3. Открываем «Контакты» (через меню «О нас»)
    open_contacts_link(home).click()
    expect(home).to_have_url(re.compile(r"/ru/contact-us"))
    close_cookie_banner(home)

    # 4. Нажимаем «Обратный звонок»
    callback = (
        home.locator('a[href="#popup:form-tr"]')
        .filter(has_text=re.compile("Обратный звонок", re.I))
        .filter(visible=True)
        .first
    )
    expect(callback).to_be_visible()
    # Поверх кнопки лежит плавающий значок «Reviews», поэтому клик мышью
    # попадает в него. Отправляем событие клика прямо в кнопку.
    callback.dispatch_event("click")

    # 5. Проверяем текст во всплывающем окне
    popup = home.locator(".t-popup_show")
    expect(popup).to_be_visible()
    # \s* между словами — на случай переноса строки (<br>) внутри текста
    expected = r"\s*".join("Запишитесь на бесплатную карьерную консультацию".split())
    expect(popup).to_contain_text(re.compile(expected))