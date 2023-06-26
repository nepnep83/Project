from behave import *
from selenium.webdriver.common.by import By


@given("a user opens the home page")
def step_impl(context):
    context.browser.get('http://127.0.0.1:5000/')


@when("a user clicks signup")
def step_impl(context):
    context.browser.find_element(By.ID, "signup").click()


@then('then they should be on the "{page}"')
def step_impl(context, page):
    assert context.browser.title == page


@when("the user enters their information")
def step_impl(context):
    context.browser.find_element(By.ID, "email").send_keys(context.table[0][0])
    context.browser.find_element(By.ID, "username").send_keys(context.table[0][1])
    context.browser.find_element(By.ID, "password").send_keys(context.table[0][2])
    context.browser.find_element(By.ID, "conf_password").send_keys(context.table[0][3])


@step("clicks submit")
def step_impl(context):
    context.browser.find_element(By.ID, "submit").click()


@when("the user enters their personal information")
def step_impl(context):
    context.browser.find_element(By.ID, "given_name").send_keys(context.table[0][0])
    context.browser.find_element(By.ID, "family_name").send_keys(context.table[0][1])
    context.browser.find_element(By.ID, "age").send_keys(context.table[0][2])


@when("a user clicks login")
def step_impl(context):
    context.browser.find_element(By.ID, "login").click()


@when("the user enters their login information")
def step_impl(context):
    context.browser.find_element(By.ID, "username").send_keys(context.table[0][0])
    context.browser.find_element(By.ID, "password").send_keys(context.table[0][1])


@step('they should see their name "{name}"')
def step_impl(context, name):
    print(context.browser.find_element(By.XPATH, "/html/body/h3").text)
    assert context.browser.find_element(By.XPATH, "/html/body/h3").text == "Hello {}".format(name)
