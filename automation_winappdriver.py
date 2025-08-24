# automation_winappdriver.py
import sys
import os
import subprocess
import time
import io
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- FIX 2: Force standard output and error streams to use UTF-8 encoding ---
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Get the absolute path to the app.py script to be tested
APP_PATH = os.path.abspath("app.py")
PYTHON_EXE_PATH = sys.executable
WINAPPDRIVER_URL = 'http://122.0.0.1:4723'

driver = None
app_process = None
try:
    print("Starting WinAppDriver test...")

    # --- Start app.py as a separate process ---
    print(f"Launching app: {PYTHON_EXE_PATH} {APP_PATH}")
    app_process = subprocess.Popen([PYTHON_EXE_PATH, APP_PATH])
    time.sleep(3) # Give the app a moment to launch

    # --- FIX 1: Use AppiumOptions instead of desired_capabilities ---
    # First, connect to the entire desktop to find our app's window handle
    desktop_options = AppiumOptions()
    desktop_options.set_capability("platformName", "Windows")
    desktop_options.set_capability("app", "Root")
    
    desktop_driver = webdriver.Remote(command_executor=WINAPPDRIVER_URL, options=desktop_options)
    
    # Find the application window by its title
    app_window = desktop_driver.find_element(AppiumBy.NAME, "Construction Assistant - Demo")
    app_window_handle = app_window.get_attribute("NativeWindowHandle")
    app_window_handle_hex = hex(int(app_window_handle))
    
    # --- Connect directly to the application window using its handle ---
    app_options = AppiumOptions()
    app_options.set_capability("platformName", "Windows")
    app_options.set_capability("appTopLevelWindow", app_window_handle_hex)
    
    driver = webdriver.Remote(command_executor=WINAPPDRIVER_URL, options=app_options)
    print("Successfully connected to the application window.")
    
    wait = WebDriverWait(driver, 10)

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
    if app_process:
        print("Terminating the application process.")
        app_process.terminate()
