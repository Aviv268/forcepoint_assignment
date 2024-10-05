from playwright.sync_api import Page
import logging
import re


class ComplicatedPage:

    URL = 'https://ultimateqa.com/complicated-page'

    def __init__(self, page: Page):
        self.page = page
        self.BUTTONS = page.locator(".et_pb_button_module_wrapper a")
        self.FACEBOOK_LINKS = page.locator("//a[@href='https://www.facebook.com/Ultimateqa1/']")
        self.SECTION_OF_SOCIAL_MEDIA = page.locator(".et_pb_row.et_pb_row_4")
        self.SECTION_OF_RANDOM_STUFF = page.locator("#Section_of_Random_Stuff")
        self.NAME_INPUT = page.locator("#et_pb_contact_name_0")
        self.EMAIL_INPUT = page.locator("#et_pb_contact_email_0")
        self.MESSAGE_TEXT_INPUT = page.locator("#et_pb_contact_message_0")
        self.MATH_EXERCISE_INPUT = page.locator("input[name='et_pb_contact_captcha_0']")
        self.MATH_QUESTION = page.locator("div[id='et_pb_contact_form_0'] p[class='clearfix']")
        self.SUBMIT_BUTTON = page.locator('form.et_pb_contact_form button[type="submit"]').nth(0)
        self.SUCCESS_MESSAGE = ".et-pb-contact-message p"

    def navigate_to_complicated_page(self):
        logging.info('Navigating to Complicated Page.')
        self.page.goto(self.URL)

    def count_buttons_in_section(self):
        logging.info("Counting buttons in 'Section of Buttons'.")
        count = self.BUTTONS.count()
        logging.info(f"Found {count} buttons in 'Section of Buttons'.")
        return count

    def verify_facebook_links(self, expected):
        links = self.SECTION_OF_SOCIAL_MEDIA.locator("a")
        for i in range(links.count()):
            href = links.nth(i).get_attribute('href')
            if 'facebook.com' in href and href != expected:
                return False
        return True

    def fill_form_and_submit(self, name, email, message):
        logging.info("Filling the form in 'Section of Random Stuff'.")
        self.SECTION_OF_RANDOM_STUFF.scroll_into_view_if_needed()

        self.NAME_INPUT.fill(name)
        self.EMAIL_INPUT.fill(email)
        self.MESSAGE_TEXT_INPUT.fill(message)

        math_captcha_question = self.MATH_QUESTION.inner_text()
        numbers = re.findall(r'\d+', math_captcha_question)
        operator = re.findall(r'[\+\-\*]', math_captcha_question)[0]
        num1 = int(numbers[0])
        num2 = int(numbers[1])

        if operator == '+':
            answer = num1 + num2
        elif operator == '-':
            answer = num1 - num2
        elif operator == '*':
            answer = num1 * num2
        else:
            logging.error('Unsupported operator in captcha.')
            raise ValueError('Unsupported operator in captcha.')

        self.MATH_EXERCISE_INPUT.fill(str(answer))

        self.SUBMIT_BUTTON.click()
        logging.info("Form submitted.")

        self.page.wait_for_selector(self.SUCCESS_MESSAGE, timeout=5000)
        success_message = self.page.locator(self.SUCCESS_MESSAGE).inner_text()
        logging.info(f"Form submission result: {success_message}")
        return success_message

