import unittest

from flask import session
from parameterized import parameterized
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.environment import Context, before_all
from tests.unittests.generic_page import Elements


class MyTestCase(unittest.TestCase):
    def setUp(self):
        context = Context()
        before_all(context)
        context.browser.get('http://127.0.0.1:5000/summary')
        self.context = context
        self.elements = Elements(context)

        self.work_history_key = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[1]/dt')
        self.work_history_value = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[1]/dd[1]')
        self.work_history_link = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[1]/dd[2]')
        self.pref_job_key = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[2]/dt')
        self.pref_job_value = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[2]/dd[1]')
        self.pref_job_link = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[2]/dd[2]')
        self.postcode_key = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[3]/dt')
        self.postcode_value = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[3]/dd[1]')
        self.postcode_link = context.browser.find_element(By.XPATH, '//*[@id="body"]/dl/div[3]/dd[2]')

        super().setUp()

    def generic_elements(self):
        # self.assertTrue(self.elements.back_link.is_displayed())
        self.assertTrue(self.postcode_key.is_displayed())
        self.assertTrue(self.elements.button.is_displayed())

        # self.assertEqual(self.elements.back_link.text, "Back")
        self.assertEqual(self.elements.heading.text, "Help us understand your work situation: check your answers")
        self.assertEqual(self.elements.button.text, "Continue")

    def test_generic_elements_are_displayed(self):
        self.generic_elements()


def is_displayed(browser, element_id):
    try:
        element = browser.find_element(By.ID, element_id)
        return element.is_displayed()
    except NoSuchElementException:
        return False


if __name__ == '__main__':
    unittest.main()

