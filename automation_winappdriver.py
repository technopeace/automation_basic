# automation_winappdriver.py
import sys
import io
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# UTF-8 stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if len(sys.argv) < 2:
    print("❌ ERROR: The absolute path to the EXE was not provided.")
    sys.exit(1)

APP_PATH = sys.argv[1]
WINAPPDRIVER_URL = "http://127.0.0.1:4723"

driver = None
try:
    print(f"Starting WinAppDriver test with app: {APP_PATH}")

    # Capabilities
    app_capabilities = {
        "platformName": "Windows",
        "appium:automationName": "Windows",
        "appium:app": APP_PATH,
        "appium:createSessionTimeout": 20000
    }
    app_options = AppiumOptions().load_capabilities(app_capabilities)

    driver = webdriver.Remote(command_executor=WINAPPDRIVER_URL, options=app_options)
    print("✅ Successfully created a session with the application.")

    wait = WebDriverWait(driver, 20)

    # Wait for main window title
    wait.until(EC.presence_of_element_located((AppiumBy.NAME, "Construction Assistant - Demo")))

    # Fill entries
    entry_fields = wait.until(EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "TEntry")))
    entry_fields[0].send_keys("Baris Kahraman")
    print("Name entered: Baris Kahraman")
    entry_fields[1].send_keys("28")
    print("Age entered: 28")

    # Save
    driver.find_element(AppiumBy.NAME, "Save").click()
    print("Save button clicked.")

    # Dialog
    dialog_text_element = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "/Window[@Name='Information']/Text"))
    )
    dialog_text = dialog_text_element.text
    print(f"Dialog text found: '{dialog_text}'")

    expected_text = "Saved!\nName: Baris Kahraman\nAge: 28"
    assert dialog_text == expected_text
    print("✅ Dialog text matches expected text.")

    driver.find_element(AppiumBy.NAME, "OK").click()
    print("Dialog closed.")

    print("🎉 WINAPPDRIVER TEST PASSED")

except Exception as e:
    print("❌ WINAPPDRIVER TEST FAILED")
    print(f"An error occurred: {e}")
    raise e
finally:
    if driver:
        driver.quit()
