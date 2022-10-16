
import logging
import os
import uuid

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def create_driver():
    # driver = Chrome("/Users/lamarr/Downloads/chromedriver")
    driver = Chrome()
    return driver