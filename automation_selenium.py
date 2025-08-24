# automation_selenium.py
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# The path to the Electron executable after it's built by electron-builder.
ELECTRON_APP_PATH = "./dist/Construction Assistant - Web.exe"

try:
    print("Starting Selenium test for Electron app...")
    options = Options()
    # Point Selenium to the Electron app's binary.
    options.binary_location = ELECTRON_APP_PATH
    
    # Modern Selenium versions manage ChromeDriver automatically.
    driver = webdriver.Chrome(options=options)
    
    # Use an explicit wait for more reliable tests.
    wait = WebDriverWait(driver, 10)

    # Find web elements by their ID and interact with them.
    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    name_field.send_keys("Baris Kahraman")
    print("Name entered: Baris Kahraman")

    age_field = driver.find_element(By.ID, "age")
    age_field.send_keys("28")
    print("Age entered: 28")

    save_button = driver.find_element(By.ID, "save-btn")
    save_button.click()
    print("Save button clicked.")

    # Wait for the success message to appear in the response div on the page.
    wait.until(EC.text_to_be_present_in_element(
        (By.ID, "response"), "Saved!"
    ))
    print("Success response verified on page.")

    # The final success message for the YAML to check.
    print("✅ SELENIUM TEST PASSED")

except Exception as e:
    print("❌ SELENIUM TEST FAILED")
    print(f"An error occurred: {e}")
    # Take a screenshot on failure for debugging.
    if 'driver' in locals():
        driver.save_screenshot('selenium-failure-screenshot.png')
        print("Failure screenshot saved as selenium-failure-screenshot.png")
finally:
    if 'driver' in locals():
        driver.quit()
    # Exit with a non-zero code on failure.
    if "e" in locals() and e:
        sys.exit(1)
    else:
        sys.exit(0)