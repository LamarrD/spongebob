from helper import upload_screenshot, LambdaContext
from headless_chrome import create_driver
from selenium.webdriver.common.by import By


def handler(_event, _context):
    """Test home page"""

    driver = create_driver()
    driver.get("https://myleg.org")
    ele = driver.find_element(By.TAG_NAME, "h1")
    print(ele.text)

    assert ele.text == "Welcome to MyLeg.org"
    driver.close()
    return "success"

if __name__ == "__main__":
    handler(None, LambdaContext())