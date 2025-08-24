# automation_selenium.py
import sys
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# -------------------------------------------------------------------
# Command line arguments:
#   1. Path to electron.exe (from node_modules)
#   2. Path to your app entry file (main.js / app_web.js)
# -------------------------------------------------------------------
if len(sys.argv) < 3:
    print("❌ ERROR: You must provide the electron.exe path and app entry file.")
    sys.exit(1)

ELECTRON_BINARY_PATH = sys.argv[1]
APP_ENTRY_FILE = sys.argv[2]

print(f"Using Electron binary: {ELECTRON_BINARY_PATH}")
print(f"Launching app entry file: {APP_ENTRY_FILE}")

CHROMEDRIVER_PATH = "./node_modules/electron-chromedriver/bin/chromedriver.exe"

driver = None
try:
    print("Starting Selenium test for Electron app...")

    options = Options()
    options.binary_location = ELECTRON_BINARY_PATH
    # Tell Electron which app entry to load
    options.add_argument(f"app={APP_ENTRY_FILE}")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    # Example UI interactions
    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    name_field.send_keys("Baris Kahraman")
    print("Name entered: Baris Kahraman")

    age_field = driver.find_element(By.ID, "age")
    age_field.send_keys("28")
    print("Age entered: 28")

    save_button = driver.find_element(By.ID, "save-btn")
    save_button.click()
    print("Save button clicked.")

    # Verify success message
    wait.until(EC.text_to_be_present_in_element((By.ID, "response"), "Saved!"))
    print("Success response verified on page.")
    print("✅ SELENIUM TEST PASSED")

except Exception as e:
    print("❌ SELENIUM TEST FAILED")
    print(f"An error occurred: {e}")
    if driver:
        driver.save_screenshot('selenium-failure-screenshot.png')
        print("Failure screenshot saved as selenium-failure-screenshot.png")
    raise e
finally:
    if driver:
        driver.quit()
