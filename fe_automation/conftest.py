from fe_automation.helpers import setup_logging
import pytest
from playwright.sync_api import sync_playwright
from fe_automation.helpers import capture_screenshot


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    setup_logging()


@pytest.fixture(scope='session')
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope='session')
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope='function')
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context, request):
    page = context.new_page()
    yield page

    if request.node.rep_call.failed:
        capture_screenshot(page, request.node.name)
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep
