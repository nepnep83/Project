import unittest

from parameterized import parameterized
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.environment import Context, before_all
from tests.unittests.generic_page import Elements


class MyTestCase(unittest.TestCase):
    def setUp(self):
        context = Context()
        before_all(context)
        context.browser.get('http://127.0.0.1:5000/')
        self.context = context
        self.elements = Elements(context)

        self.job_title = context.browser.find_element(By.ID, "job_title")
        self.job_title_label = context.browser.find_element(By.XPATH, '//*[@id="conditional-radio"]/div/label')
        self.job_title_heading = context.browser.find_element(By.XPATH, '//*[@id="conditional-radio"]/h2')
        self.job_title_hint = context.browser.find_element(By.XPATH, '//*[@id="conditional-radio"]/p')


        super().setUp()

    def generic_elements(self):
        self.assertTrue(self.elements.heading.is_displayed())
        self.assertTrue(self.elements.radio_hint.is_displayed())
        self.assertTrue(self.elements.button.is_displayed())

        self.assertEqual(self.elements.heading.text, "Your work history")
        self.assertEqual(self.elements.fieldset_heading.text, "Have you worked previously?")
        self.assertEqual(self.elements.radio_hint.text, "Select one option.")
        self.assertEqual(self.elements.radio_label.text, "Yes")
        self.assertEqual(self.elements.radio_label2.text, "No")
        self.assertEqual(self.elements.button.text, "Continue")

    def test_generic_elements_are_displayed(self):
        self.generic_elements()

    @parameterized.expand([
        ("Invalid character", '❤️', "Inputs must only contain alphabetical and selected special characters"),
        ("More than 100 characters", 'a' * 101, "Input must not be more than 100 characters"),
        ("Invalid character", '', "This field is required."),
    ])
    def test_errors_when_invalid_input(self, name, invalid_input, error_message):
        self.generic_elements()
        self.elements.radio.click()
        self.job_title.send_keys(invalid_input)
        self.elements.button.click()
        self.assertEqual("Error:\n" + error_message,
                         self.context.browser.find_element(By.ID, 'job_title-error').text)

    @parameterized.expand([
        ("Invalid character", '❤️'),
        ("More than 100 characters", 'a' * 101),
        ("Invalid character", ''),
    ])
    def test_job_title_input_not_checked_when_n(self, name, input_):
        self.generic_elements()
        self.elements.radio.click()
        self.job_title.send_keys(input_)
        self.elements.radio_2.click()
        self.assertFalse(self.job_title.is_displayed())
        self.assertFalse(self.job_title_label.is_displayed())
        self.elements.button.click()
        self.assertFalse(is_displayed(self.context.browser, 'job_title-error'))

    def test_elements_displayed_correctly_when_yes_selected(self):
        self.elements.radio.click()

        self.generic_elements()

        self.assertTrue(self.job_title.is_displayed())
        self.assertTrue(self.job_title_label.is_displayed())
        self.assertTrue(self.job_title_heading.is_displayed())
        self.assertTrue(self.job_title_hint.is_displayed())
        self.assertEqual(self.job_title_label.text, "Job title")
        self.assertEqual(self.job_title_heading.text, "Tell us about your previous jobs")
        self.assertEqual(self.job_title_hint.text,
                         "Your previous work is helpful to know about, even if you do a different type of work now.")


def is_displayed(browser, element_id):
    try:
        element = browser.find_element(By.ID, element_id)
        return element.is_displayed()
    except NoSuchElementException:
        return False


if __name__ == '__main__':
    unittest.main()
