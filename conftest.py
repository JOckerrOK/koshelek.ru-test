import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def browser():
    """
    Фикстура для открытия браузера
    :return:
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context(
            ignore_https_errors=True)
        page = context.new_page()
        yield page
        context.close()
        browser.close()
