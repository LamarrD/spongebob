from helper import upload_screenshot, LambdaContext
from headless_chrome import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handler(event, context):
    """Test characters page."""

    try:
        # Navigate from home page to characters page
        driver = create_driver()
        driver.get("http://myleg.org")
        upload_screenshot(context.aws_request_id, driver, "home")
        driver.find_element(By.ID, "characters").click()
        upload_screenshot(context.aws_request_id, driver, "characters-page")

        # Wait for characters to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, 'character-list')))
        upload_screenshot(context.aws_request_id, driver, "characters-list")

        # Get a random fact for one of the characters
        # NOTE: clicking with javascript to avoid this bug https://stackoverflow.com/questions/37879010/selenium-debugging-element-is-not-clickable-at-point-x-y
        karen = driver.find_element(By.ID, 'random-karen_plankton')
        driver.execute_script("arguments[0].click();", karen)
        fact = wait.until(EC.visibility_of_element_located((By.ID, 'random-fact-body')))
        upload_screenshot(context.aws_request_id, driver, "karen_fact")
        assert len(fact.text) > 10

        # Close the random fact modal
        modal_header = driver.find_element(By.ID, 'random-fact-header')
        modal_header.find_element(By.TAG_NAME, 'button').click()
        wait.until(EC.invisibility_of_element_located((By.ID, 'random-fact-body')))
        driver.quit()
    except Exception as e:
        for entry in driver.get_log('browser'):
            print(entry)
        raise e
        
    return "success"



if __name__ == "__main__":
    handler(None, LambdaContext())