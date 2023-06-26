import unittest

from parameterized import parameterized
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.environment import Context, before_all
from tests.unittests.generic_page import Elements


class MyTestCase(unittest.TestCase):
    def setUp(self):
        context = Context()
        before_all(context)
        context.browser.get('http://127.0.0.1:5000/preferred')
        self.context = context
        self.elements = Elements(context)

        # self.pref_job_error =
        self.pref_job = context.browser.find_element(By.ID, "pref_job")
        self.pref_job_label = context.browser.find_element(By.XPATH, '//*[@id="conditional-radio"]/div/label')

        super().setUp()

    def test_generic_elements(self):
        self.assertTrue(self.elements.back_link.is_displayed())
        self.assertTrue(self.elements.heading.is_displayed())
        self.assertTrue(self.elements.body.is_displayed())
        self.assertTrue(self.elements.fieldset_heading.is_displayed())
        self.assertTrue(self.elements.radio_hint.is_displayed())
        self.assertTrue(self.elements.button.is_displayed())
        self.assertFalse(self.pref_job.is_displayed())
        self.assertFalse(self.pref_job_label.is_displayed())

        self.assertEqual(self.elements.back_link.text, "Back")
        self.assertEqual(self.elements.heading.text, "Your preferred jobs")
        self.assertEqual(self.elements.body.text,
                         "We want to know if there are specific jobs or types of work you're interested in, "
                         "even if you think you do not have the necessary skills and experience right now.")
        self.assertEqual(self.elements.fieldset_heading.text,
                         "Do you know what you'd like to do now or in the near future?")
        self.assertEqual(self.elements.radio_hint.text, "Select one option.")
        self.assertEqual(self.elements.radio_label.text, "Yes")
        self.assertEqual(self.elements.radio_label2.text, "No")
        self.assertEqual(self.elements.button.text, "Continue")

    @parameterized.expand([
        ("Invalid character", '❤️', "Inputs must only contain alphabetical and selected special characters"),
        ("More than 100 characters", 'a' * 101, "Input must not be more than 100 characters"),
        ("Invalid character", '', "This field is required."),
    ])
    def test_errors_when_invalid_input(self, name, invalid_input, error_message):
        self.elements.radio.click()
        self.pref_job.send_keys(invalid_input)
        self.elements.button.click()
        self.assertEqual("Error:\n" + error_message,
                         self.context.browser.find_element(By.ID, 'pref_job-error').text)

    def test_pref_job_input_not_checked_when_no_1(self):
        self.elements.radio.click()
        self.pref_job.send_keys('❤️')
        self.elements.radio_2.click()
        self.elements.button.click()
        self.assertFalse(is_displayed(self.context.browser, 'pref_job-error'))

    def test_pref_job_input_not_checked_when_no_2(self):
        self.elements.radio.click()
        self.pref_job.send_keys('a'*101)
        self.elements.radio_2.click()
        self.elements.button.click()
        self.assertFalse(is_displayed(self.context.browser, 'pref_job-error'))

    def test_pref_job_input_not_checked_when_no_3(self):
        self.elements.radio.click()
        self.pref_job.send_keys('️')
        self.elements.radio_2.click()
        self.elements.button.click()
        self.assertFalse(is_displayed(self.context.browser, 'pref_job-error'))

    def test_elements_displayed_correctly_when_yes_selected(self):

        self.elements.radio.click()
        self.assertEqual(self.pref_job_label.text, "Job")
        self.assertTrue(is_displayed(self.context.browser, 'pref_job-hint'))


def is_displayed(browser, element_id):
    try:
        element = browser.find_element(By.ID, element_id)
        return element.is_displayed()
    except NoSuchElementException:
        return False

if __name__ == '__main__':
    unittest.main()
