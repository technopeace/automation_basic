# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys
import traceback  # Import the traceback module for detailed error logging

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
# This block ensures the script finds the Tesseract executable and its data files,
# regardless of whether it's running as a bundled .exe or a standard .py file.
if getattr(sys, "frozen", False):
    # If running as a bundled executable, the path is the directory of the executable itself.
    application_path = os.path.dirname(sys.executable)
else:
    # If running as a standard .py script, the path is the directory of the script file.
    application_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the Tesseract executable, assuming it's in a 'tesseract' subfolder.
tesseract_path = os.path.join(application_path, "tesseract", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Define the path to the 'tessdata' directory.
tessdata_dir_path = os.path.join(application_path, "tesseract", "tessdata")
# --- END OF CONFIGURATION ---


print("Automation will start in 5 seconds...")
time.sleep(5)

try:
    # --- Step 1: Find and Fill the Input Fields ---
    print("Searching for the name label...")

    # Construct the full path to the image file to ensure it's found.
    isim_label_path = os.path.join(application_path, "isim_label.png")

    # Tell pyautogui to search for the image using its full path.
    isim_label_location = pyautogui.locateCenterOnScreen(
        isim_label_path, confidence=0.4
    )

    if isim_label_location:
        # First, click the label itself to ensure the target application window is active.
        pyautogui.click(isim_label_location)
        print("Clicked the 'Name:' label to activate the window.")
        time.sleep(0.3)  # A brief pause for the window to come into focus.

        # Now, click on the text box, which is slightly below the label.
        pyautogui.click(isim_label_location.x, isim_label_location.y + 35)
        print("Clicked on the name input field.")
        time.sleep(0.5)

        # Use the copy-paste method for reliability. Changed to English name.
        pyperclip.copy("John Doe")
        # Automatically select the correct paste shortcut for the OS.
        pyautogui.hotkey("ctrl" if sys.platform == "win32" else "command", "v")
        print("Name entered: John Doe")
    else:
        # If the label is not found, the script cannot proceed.
        print(f"ERROR: Could not find '{isim_label_path}' on the screen.")
        sys.exit(1)  # Exit with an error code.

    time.sleep(0.5)

    # Move focus to the next input field (Age).
    pyautogui.press("tab")
    time.sleep(0.5)

    # Enter the age using the same reliable copy-paste method.
    pyperclip.copy("35")
    pyautogui.hotkey("ctrl" if sys.platform == "win32" else "command", "v")
    print("Age entered: 35")
    time.sleep(0.5)

    # --- Step 2: Activate the Save Button ---
    # Move focus from the Age field to the Save button.
    pyautogui.press("tab")
    time.sleep(0.5)
    # Activate the focused button using the space bar (more reliable than clicking).
    pyautogui.press("space")
    print("Save action activated!")
    time.sleep(1.5)  # Wait for the confirmation dialog to appear.

    # --- Step 3: Read the Result from the Dialog Box ---
    print("Assuming the dialog box appears in the center of the screen...")
    # Get screen dimensions to calculate the center.
    screenWidth, screenHeight = pyautogui.size()

    # Define a region in the center of the screen where the dialog is expected.
    dialog_width = 400
    dialog_height = 300
    dialog_x = int((screenWidth - dialog_width) / 2)
    # We offset the Y-coordinate slightly upwards to better capture the dialog.
    dialog_y = int((screenHeight - dialog_height) / 2) - 50
    dialog_region = (dialog_x, dialog_y, dialog_width, dialog_height)

    # Take a screenshot of only that region.
    text_screenshot = pyautogui.screenshot(region=dialog_region)

    print("Sending screenshot to Tesseract for OCR...")
    
    # Normalize the path for the command line.
    tessdata_dir_path_normalized = tessdata_dir_path.replace('\\', '/')
    
    # Pass the clean, normalized path directly in the config.
    custom_config = f'--oem 3 --psm 6 --tessdata-dir "{tessdata_dir_path_normalized}"'
    
    # Perform OCR on the screenshot using the English language data.
    text = pytesseract.image_to_string(
        text_screenshot, lang="eng", config=custom_config
    )
    # Clean the OCR result from extra spaces and line breaks.
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    # --- Step 4: Close the Dialog Box ---
    # Press Enter to click the default 'OK' button in the dialog.
    pyautogui.press("enter")
    print("\n🎉 Automation completed successfully! 🎉")
    sys.exit(0)  # Exit with a success code.

except Exception as e:
    # Prints the full technical error details for debugging.
    print(f"An unexpected error occurred:")
    traceback.print_exc()
    sys.exit(1)  # Exit with an error code.
