# automation_winappdriver.py
import sys
import os
import io
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Force standard output and error streams to use UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Get the absolute path to the launcher script from the command line
if len(sys.argv) < 2:
    print("❌ ERROR: The absolute path to the launcher script (.bat) was not provided.")
    sys.exit(1)
APP_LAUNCHER_PATH = sys.argv[1]

WINAPPDRIVER_URL = 'http://127.0.0.1:4723'

driver = None
try:
    print(f"Starting WinAppDriver test with launcher: {APP_LAUNCHER_PATH}")

    # --- THE FIX: Let WinAppDriver launch the app directly ---
    # This creates a single, fast, and direct connection.
    app_options = AppiumOptions()
    app_options.set_capability("platformName", "Windows")
    app_options.set_capability("appium:automationName", "Windows")
    app_options.set_capability("appium:app", APP_LAUNCHER_PATH)
    app_options.set_capability("appium:createSessionTimeout", "20000") # 20 seconds timeout

    driver = webdriver.Remote(command_executor=WINAPPDRIVER_URL, options=app_options)
    print("Successfully created a session with the application.")
    
    # Wait for the main window to be ready
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((AppiumBy.NAME, "Construction Assistant - Demo")))

    # --- Interact with elements using Accessibility Properties ---
    entry_fields = wait.until(EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "TEntry")))
    
    entry_fields[0].send_keys("Baris Kahraman")
    print("Name entered: Baris Kahraman")
    
    entry_fields[1].send_keys("28")
    print("Age entered: 28")

    driver.find_element(AppiumBy.NAME, "Save").click()
    print("Save button clicked.")

    dialog_text_element = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "/Window[@Name='Information']/Text")
    ))
    dialog_text = dialog_text_element.text
    print(f"Dialog text found: '{dialog_text}'")

    expected_text = "Saved!\nName: Baris Kahraman\nAge: 28"
    assert dialog_text == expected_text
    print("Dialog text matches expected text.")

    driver.find_element(AppiumBy.NAME, "OK").click()
    print("Dialog closed.")
    
    print("✅ WINAPPDRIVER TEST PASSED")

except Exception as e:
    print("❌ WINAPPDRIVER TEST FAILED")
    print(f"An error occurred: {e}")
    raise e
finally:
    # Clean up resources
    if driver:
        driver.quit()

