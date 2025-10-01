
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.app import create_app



class TestSecureNote:

    def test_add_valid_note(self, driver, selenium_server):
        """Test Case 1: Adding a Valid Notes"""
        print("Running Test: Adding a Valid Note")
        driver.get(selenium_server)

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
        
        #Verify note appears in list
        notes_list = driver.find_element(By.TAG_NAME, "ul").text
        assert "Automated Test Note" in notes_list
    
    def test_add_note_empty_content(self,driver,selenium_server):
        """Test Case 2: Adding a note with empty content"""
        print("Running Test: Adding a note with empty content")
        driver.get(selenium_server)

        title_field = driver.find_element(By.NAME, "title")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        title_field.send_keys("Note with No Content")
        submit_button.click()

        #Wait for the success message
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error"))
        )
        error_message = driver.find_element(By.CLASS_NAME, "error").text
        assert "empty" in error_message.lower()
    
    def test_add_note_empty_title(self,driver,selenium_server):
        """Test Case 2: Adding a note with empty content"""
        print("Running Test: Adding a note with empty content")
        driver.get(selenium_server)

        content_field = driver.find_element(By.NAME, "content")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        content_field.send_keys("This note has no title provided.")
        submit_button.click()

        #Wait for the success message
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )

        #Verify note appears with default title
        notes_list = driver.find_element(By.TAG_NAME, "ul").text
        assert "Untitled" in notes_list
        assert "This note has no title provided" in notes_list

    def test_delete_note(self, driver, selenium_server):
        """Test Case 4: Deleting a Note"""
        print("Running Test: Deleting a Note")
        driver.get(selenium_server)
        
        # First, add a note to delete
        title_field = driver.find_element(By.NAME, "title")
        content_field = driver.find_element(By.NAME, "content")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        note_title = "Note to Delete"
        note_content = "This note will be deleted."

        title_field.send_keys(note_title)
        content_field.send_keys(note_content)
        submit_button.click()

        # Wait for the note to be added
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )

        notes_list = driver.find_element(By.TAG_NAME, "ul")
        note_text_before = notes_list.text

        #Verify note is in the list.
        assert note_title in note_text_before, f"Note '{note_title}' not found in list"

        specific_delete_link = driver.find_element(By.XPATH, f"//li[contains(., '{note_title}')]//a[contains(@href, '/delete/')]")
        specific_delete_link.click()
        
        # Wait for the success message
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )
        success_msg = driver.find_element(By.CLASS_NAME, "success").text
        assert "deleted" in success_msg.lower()
        
        # Verify note is removed from list
        note_text_after = driver.find_element(By.TAG_NAME, "ul").text
        assert note_title not in note_text_after, f" Note '{note_title}' still in list after deletion"

if __name__ == "__main__":

    pytest.main([__file__, "-v"])