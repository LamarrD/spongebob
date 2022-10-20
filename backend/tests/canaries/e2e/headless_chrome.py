
import logging
import os
import uuid

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = Chrome(options=options)
    return driver