import sys
import io
import time
from appium import webdriver
from appium.options.windows import WindowsOptions
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# --- FIX #2: Add UTF-8 support to prevent encoding errors ---
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WinAppDriver URL
WINAPPDRIVER_URL = "http://127.0.0.1:4723"

if len(sys.argv) < 2:
    print("❌ ERROR: Missing EXE path argument.")
    sys.exit(1)

exePath = sys.argv[1]
print(f"Starting WinAppDriver test with app: {exePath}")

driver = None
try:
    # --- FIX #1: Use the dedicated '.app' property of WindowsOptions ---
    # This is the modern, reliable way to set the application path.
    app_options = WindowsOptions()
    app_options.app = exePath
    app_options.set_capability("appium:createSessionTimeout", 20000)

    # --- Start session ---
    driver = webdriver.Remote(
        command_executor=WINAPPDRIVER_URL,
        options=app_options
    )

    print("✅ Session created successfully with WinAppDriver.")

    # --- Wait for app to load ---
    # The app being tested is the automation script itself, which runs and closes.
    # We will wait a few seconds to ensure it has time to execute.
    print("Waiting for automation EXE to complete...")
    time.sleep(15) # Wait for the PyAutoGUI script to perform its actions and close

    # Since the app closes itself, we can't test its UI elements here.
    # We will rely on the output check in the YAML file.
    # This script's only job is to successfully launch the EXE.
    print("🎉 WINAPPDRIVER TEST PASSED")

except WebDriverException as e:
    print(f"❌ WINAPPDRIVER TEST FAILED\nAn error occurred: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
finally:
    # If the driver session was created, quit it.
    if driver:
        driver.quit()
