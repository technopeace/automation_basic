# automation_winappdriver.py
import sys
import os
import subprocess
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get the absolute path to the app.py script to be tested
APP_PATH = os.path.abspath("app.py")
PYTHON_EXE_PATH = sys.executable
WINAPPDRIVER_URL = 'http://127.0.0.1:4723'

driver = None
app_process = None
try:
    print("Starting WinAppDriver test...")

    # --- Start app.py as a separate process ---
    # WinAppDriver needs the app to be running to connect to it.
    print(f"Launching app: {PYTHON_EXE_PATH} {APP_PATH}")
    app_process = subprocess.Popen([PYTHON_EXE_PATH, APP_PATH])
    time.sleep(3) # Give the app a moment to launch

    # --- Configure WinAppDriver ---
    # First, connect to the entire desktop to find our app's window handle
    desktop_caps = {
        "platformName": "Windows",
        "app": "Root",
    }
    desktop_driver = webdriver.Remote(command_executor=WINAPPDRIVER_URL, desired_capabilities=desktop_caps)
    
    # Find the application window by its title
    app_window = desktop_driver.find_element(AppiumBy.NAME, "Construction Assistant - Demo")
    app_window_handle = app_window.get_attribute("NativeWindowHandle")
    app_window_handle_hex = hex(int(app_window_handle))
    
    # --- Connect directly to the application window ---
    app_caps = {
        "platformName": "Windows",
        "appTopLevelWindow": app_window_handle_hex, # Attach to our specific window
    }
    driver = webdriver.Remote(command_executor=WINAPPDRIVER_URL, desired_capabilities=app_caps)
    print("Successfully connected to the application window.")
    
    wait = WebDriverWait(driver, 10)

    # --- Interact with elements using Accessibility Properties ---
    # Tkinter Entry fields have a ClassName of 'TEntry'. We find them by order.
    entry_fields = wait.until(EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "TEntry")))
    
    # First TEntry is for Name
    entry_fields[0].send_keys("Baris Kahraman")
    print("Name entered: Baris Kahraman")
    
    # Second TEntry is for Age
    entry_fields[1].send_keys("28")
    print("Age entered: 28")

    # Find the button by its text (which is its 'Name' property)
    driver.find_element(AppiumBy.NAME, "Save").click()
    print("Save button clicked.")

    # Wait for the dialog box to appear and get its text
    # The dialog content is a StaticText element (TLabel in Tkinter) inside the "Information" window
    dialog_text_element = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "/Window[@Name='Information']/Text")
    ))
    dialog_text = dialog_text_element.text
    print(f"Dialog text found: '{dialog_text}'")

    expected_text = "Saved!\nName: Baris Kahraman\nAge: 28"
    assert dialog_text == expected_text
    print("Dialog text matches expected text.")

    # Close the dialog by clicking the "OK" button
    driver.find_element(AppiumBy.NAME, "OK").click()
    print("Dialog closed.")
    
    # Final success message for the YAML to check
    print("✅ WINAPPDRIVER TEST PASSED")

except Exception as e:
    print("❌ WINAPPDRIVER TEST FAILED")
    print(f"An error occurred: {e}")
    raise e # Re-raise the exception to ensure the script exits with an error code
finally:
    # Clean up resources
    if driver:
        driver.quit()
    if app_process:
        print("Terminating the application process.")
        app_process.terminate()

