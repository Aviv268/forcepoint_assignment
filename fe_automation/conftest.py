import logging
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    logging.basicConfig(
        filename='fe_automation/logs/test.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info('Logging setup complete.')


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


@pytest.fixture(scope='function')
def page(context):
    page = context.new_page()
    yield page
    page.close()


def pytest_terminal_summary(terminalreporter):
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    print("\nTest Summary:")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
