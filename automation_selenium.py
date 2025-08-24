# automation_selenium.py
import sys
import io

# --- FIX 2: Force standard output and error streams to use UTF-8 encoding ---
# This prevents UnicodeEncodeError when printing emojis or special characters.
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- FIX 1: Path now matches the `name` from package.json, which is more reliable ---
ELECTRON_APP_PATH = "./dist/construction-assistant-web.exe"

# Point to the compatible ChromeDriver bundled with Electron.
CHROMEDRIVER_PATH = "./node_modules/electron-chromedriver/bin/chromedriver.exe"

driver = None
try:
    print("Starting Selenium test for Electron app...")
    options = Options()
    # Point Selenium to the Electron app's binary.
    options.binary_location = ELECTRON_APP_PATH
    
    # Create a Service object pointing to the correct driver.
    service = Service(executable_path=CHROMEDRIVER_PATH)
    
    # Launch the driver.
    driver = webdriver.Chrome(service=service, options=options)
    
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
    if driver:
        driver.save_screenshot('selenium-failure-screenshot.png')
        print("Failure screenshot saved as selenium-failure-screenshot.png")
    # Re-raise the exception to make sure the script exits with an error code.
    raise e
finally:
    if driver:
        driver.quit()