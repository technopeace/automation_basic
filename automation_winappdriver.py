import sys
import time
from appium import webdriver
from appium.options.windows import WindowsOptions
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# WinAppDriver URL
WINAPPDRIVER_URL = "http://127.0.0.1:4723"

if len(sys.argv) < 2:
    print("❌ ERROR: Missing EXE path argument.")
    sys.exit(1)

exePath = sys.argv[1]
print(f"Starting WinAppDriver test with app: {exePath}")

try:
    # --- Capabilities ---
    app_options = WindowsOptions()
    # IMPORTANT: WinAppDriver expects 'app', not 'appium:app'
    app_options.set_capability("app", exePath)

    # --- Start session ---
    driver = webdriver.Remote(
        command_executor=WINAPPDRIVER_URL,
        options=app_options
    )

    print("✅ Session created with WinAppDriver.")

    # --- Wait for app to load ---
    time.sleep(3)

    # --- Example test: interact with window ---
    try:
        # Find main window
        main_window = driver.find_element("xpath", "/*")
        print("✅ Main window located.")

        # You can extend with real UI tests here
        print("🎉 WINAPPDRIVER TEST PASSED")

    except NoSuchElementException:
        print("❌ Could not find main window element.")
        sys.exit(1)

    finally:
        driver.quit()

except WebDriverException as e:
    print(f"❌ WINAPPDRIVER TEST FAILED\nAn error occurred: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
