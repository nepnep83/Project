import unittest

from selenium.webdriver.common.by import By

from tests.environment import Context, before_all
from tests.unittests.generic_page import Elements


class MyTestCase(unittest.TestCase):
    def setUp(self):
        context = Context()
        before_all(context)
        context.browser.get('http://127.0.0.1:5000/preferred')
        self.elements = Elements(context)

        # self.pref_job_error = context.browser.find_element(By.ID, 'pref_job-error')
        self.pref_job = context.browser.find_element(By.ID, "pref_job")
        # self.invalid_input = context.browser.find_element(By.ID, 'pref_job').click().send_keys(context.table[0][0])


        super().setUp()

    def test_generic_elements(self):
        self.assertEqual(self.elements.back_link.text, "Back")
        self.assertEqual(self.elements.heading.text, "Your preferred jobs")
        self.assertEqual(self.elements.body.text,
                         "We want to know if there are specific jobs or types of work you're interested in, even if you think you do not have the necessary skills and experience right now.")
        self.assertEqual(self.elements.fieldset_heading.text,
                         "Do you know what you'd like to do now or in the near future?")
        self.assertEqual(self.elements.radio_hint.text, "Select one option.")
        self.assertEqual(self.elements.button.text, "Continue")

    def test_errors_when_invalid_input(self):
        # self.assertWarnsRegex(self.invalid_input, self.pref_job)
        n


if __name__ == '__main__':
    unittest.main()
