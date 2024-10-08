import pytest
from fe_automation.pages.complicated_page import ComplicatedPage
import logging
import allure


@allure.step("test_navigate_to_complicated_page")
def test_navigate_to_complicated_page(page):
    logging.info("Starting test: test_navigate_to_complicated_page")
    complicated_page = ComplicatedPage(page)
    complicated_page.navigate_to_complicated_page()
    assert page.url == ComplicatedPage.URL, "Failed to navigate to the correct URL."
    expected_title = "Complicated Page - Ultimate QA"
    assert page.title() == expected_title, "Page title does not match expected title."
    logging.info("Test 'test_navigate_to_complicated_page' passed.")


@allure.step("test_count_buttons")
def test_count_buttons(page):
    logging.info("Starting test: test_count_buttons")
    complicated_page = ComplicatedPage(page)
    complicated_page.navigate_to_complicated_page()
    count = complicated_page.count_buttons_in_section()
    assert count == 6, f"Expected 12 buttons, but found {count}."
    logging.info("Test 'test_count_buttons' passed.")


@allure.step("test_verify_facebook_links")
def test_verify_facebook_links(page):
    logging.info("Starting test: test_verify_facebook_links")
    complicated_page = ComplicatedPage(page)
    complicated_page.navigate_to_complicated_page()
    expected_href = 'https://www.facebook.com/Ultimateqa1/'
    all_correct = complicated_page.verify_facebook_links(expected_href)
    assert all_correct, "Not all Facebook links have the expected href."
    logging.info("Test 'test_verify_facebook_links' passed.")


@allure.step("test_fill_form_and_submit")
@pytest.mark.parametrize("name, email, message", [
    ("Aviv Almoznino", "aviv123@forcepoint.com", "This is an automated test message."),
    ("Will Smith", "will.smith@gmail.com", "The legend 2"),
])
def test_fill_form_and_submit(page, name, email, message):
    logging.info(f"Starting test: test_fill_form_and_submit with name={name}, email={email}, message={message}")
    complicated_page = ComplicatedPage(page)
    complicated_page.navigate_to_complicated_page()
    result = complicated_page.fill_form_and_submit(name, email, message)
    assert 'Thanks for contacting us' == result, f"Form submission failed: {result}"
    logging.info("Test 'test_fill_form_and_submit' passed.")
