import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app import create_app


class Context:
    def __init__(self):
        self.browser = None

    pass


CHROME_DRIVER = os.path.join(os.path.join(os.path.dirname(__file__), 'driver'), 'chromedriver.exe')

chrome_options = Options()
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")


def before_all(context):
    context.browser = webdriver.Chrome(options=chrome_options)
    context.browser.set_page_load_timeout(time_to_wait=200)
