from headless_chrome import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handler(_event, _context):
    """Test characters page."""

    # Navigate from home page to characters page
    driver = create_driver()
    driver.get("http://myleg.org")
    driver.find_element(By.ID, "characters").click()

    # Wait for characters to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, 'character-list')))

    # Get a random fact for one of the characters
    driver.find_element(By.ID, 'random-karen_plankton').click()
    fact = wait.until(EC.visibility_of_element_located((By.ID, 'random-fact-body')))
    assert "Karen" in fact.text

    # Close the random fact modal
    modal_header = driver.find_element(By.ID, 'random-fact-header')
    modal_header.find_element(By.TAG_NAME, 'button').click()
    wait.until(EC.invisibility_of_element_located((By.ID, 'random-fact-body')))

    return "success"


if __name__ == "__main__":
    handler(None, None)