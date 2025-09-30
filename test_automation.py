from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#Use Chrome options to suppress logging
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-dev-shm-usuage')
chrome_options.add_argument('--no-sandbox')
#Set up the driver(using Chrome)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://127.0.0.1:5000")

def test_add_valid_note():
    """Test Case 1: Adding a Valid Note"""
    print("Running Test: Adding a valid note")
    try:
        title_field = driver.find_element(By.NAME, "title")
        content_field = driver.find_element(By.NAME, "content")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        title_field.send_keys("Automated Test Note")
        content_field.send_keys("This note was added by Selenium")
        submit_button.click()

        #Wait for the success message
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )
        success_message = driver.find_element(By.CLASS_NAME, "success").text
        assert "success" in success_message.lower()
        print(" -> PASSED")
    except Exception as e:
        print(f" -> FAILED: {e}")

def test_add_note_empty_content():
    """Test Case 2: Adding a note with empty content"""
    print("Running Test: Adding a note with empty content")

    try:
        driver.refresh()
        title_field = driver.find_element(By.NAME, "title")
        # content_field = driver.find_element(By.NAME, "content")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        title_field.send_keys("Automated Test Note w/ empty Content")
        # content_field.send_keys("This note was added by Selenium")
        submit_button.click()

        #Wait for the success message
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error"))
        )
        error_message = driver.find_element(By.CLASS_NAME, "error").text
        assert "empty" in error_message.lower()
        print(" -> PASSED (Error message shown)")
    except Exception as e:
        print(f" -> FAILED: {e}")

if __name__ == "__main__":

    test_add_valid_note()
    test_add_note_empty_content()

    #See result then quit
    time.sleep(3)
    driver.quit()