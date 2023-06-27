from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class Elements:
    def __init__(self, context):
        self.back_link = find_element(context.browser, By.CLASS_NAME, "govuk-back-link")
        self.main_content = find_element(context.browser, By.ID, "main-content")
        self.heading = find_element(context.browser, By.ID, "heading")
        self.body = find_element(context.browser, By.ID, "body")
        self.fieldset_heading = find_element(context.browser, By.CLASS_NAME, "govuk-fieldset__heading")
        self.radio_hint = find_element(context.browser, By.ID, "radio-hint")
        self.radio = find_element(context.browser, By.ID, "radio")
        self.radio_label = find_element(context.browser, By.XPATH,
                                                        '//*[@id="main-content"]/div/div/form/div/fieldset/div[2]/div[1]/label')
        self.radio_label2 = find_element(context.browser, By.XPATH,
                                                         '//*[@id="main-content"]/div/div/form/div/fieldset/div[2]/div[3]/label')
        self.radio_2 = find_element(context.browser, By.ID, "radio-2")
        self.button = find_element(context.browser, By.ID, "submit")

    pass


def find_element(browser, by, element):
    try:
        return browser.find_element(by, element)
    except NoSuchElementException:
        return None
