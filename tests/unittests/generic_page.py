from selenium.webdriver.common.by import By


class Elements:
    def __init__(self, context):
        self.back_link = context.browser.find_element(By.CLASS_NAME, "govuk-back-link")
        self.main_content = context.browser.find_element(By.ID, "main-content")
        self.heading = context.browser.find_element(By.ID, "heading")
        self.body = context.browser.find_element(By.ID, "body")
        self.fieldset_heading = context.browser.find_element(By.CLASS_NAME, "govuk-fieldset__heading")
        self.radio_hint = context.browser.find_element(By.ID, "radio-hint")
        self.radio = context.browser.find_element(By.ID, "radio")
        self.radio_2 = context.browser.find_element(By.ID, "radio-2")
        self.button = context.browser.find_element(By.ID, "submit")


    pass
