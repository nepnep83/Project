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
        context.browser.get('http://127.0.0.1:5000/postcode')
        self.context = context
        self.elements = Elements(context)

        self.postcode = context.browser.find_element(By.ID, "postcode")
        self.postcode_label = context.browser.find_element(By.XPATH, '//*[@id="main-content"]/form/div/div/div/label')

        super().setUp()

    def generic_elements(self):
        self.assertTrue(self.elements.back_link.is_displayed())
        self.assertTrue(self.elements.heading.is_displayed())
        self.assertTrue(self.elements.button.is_displayed())
        self.assertTrue(self.postcode.is_displayed())

        self.assertEqual(self.elements.back_link.text, "Back")
        self.assertEqual(self.elements.heading.text, "Your postcode")
        self.assertEqual(self.postcode_label.text, "What is your current postcode?")
        self.assertEqual(self.elements.button.text, "Continue")

    def test_generic_elements_are_displayed(self):
        self.generic_elements()

    @parameterized.expand([
        ("Invalid character", '❤️', "Inputs must only contain alphanumeric characters"),
        ("More than 100 characters", 'a' * 9, "Postcode must not be more than 8 character long"),
        ("Invalid character", '', "This field is required."),
    ])
    def test_errors_when_invalid_input(self, name, invalid_input, error_message):
        self.generic_elements()
        self.postcode.send_keys(invalid_input)
        self.elements.button.click()
        self.assertEqual("Error:\n" + error_message, self.context.browser.find_element(By.ID, 'postcode-error').text)


def is_displayed(browser, element_id):
    try:
        element = browser.find_element(By.ID, element_id)
        return element.is_displayed()
    except NoSuchElementException:
        return False


if __name__ == '__main__':
    unittest.main()

