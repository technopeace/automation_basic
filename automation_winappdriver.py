import sys
import io
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

# --- Add UTF-8 support to prevent encoding errors ---
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WinAppDriver URL
WINAPPDRIVER_URL = "http://127.0.0.1:4723"

if len(sys.argv) < 2:
    print("❌ ERROR: Missing appTopLevelWindow (HWND in HEX).")
    sys.exit(1)

APP_WINDOW_HANDLE = sys.argv[1]
print(f"Starting WinAppDriver test with appTopLevelWindow: {APP_WINDOW_HANDLE}")

driver = None
try:
    # --- Use appTopLevelWindow instead of app ---
    capabilities = {
        "platformName": "Windows",
        "appium:automationName": "Windows",
        "appium:appTopLevelWindow": APP_WINDOW_HANDLE,
        "appium:createSessionTimeout": 20000
    }
    app_options = AppiumOptions().load_capabilities(capabilities)

    driver = webdriver.Remote(
        command_executor=WINAPPDRIVER_URL,
        options=app_options
    )

    print("✅ Session created successfully with WinAppDriver.")

    # --- Wait for the main window elements ---
    wait = WebDriverWait(driver, 20)

    # Find entry fields by class name
    entry_fields = wait.until(EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "TEntry")))

    entry_fields[0].send_keys("Baris Kahraman")
    print("Name entered: Baris Kahraman")

    entry_fields[1].send_keys("28")
    print("Age entered: 28")

    driver.find_element(AppiumBy.NAME, "Save").click()
    print("Save button clicked.")

    # Verify the dialog text
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

    print("🎉 WINAPPDRIVER TEST PASSED")

except (WebDriverException, TimeoutException) as e:
    print(f"❌ WINAPPDRIVER TEST FAILED\nAn error occurred: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    sys.exit(1)
finally:
    if driver:
        driver.quit()
