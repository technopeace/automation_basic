# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
# This block ensures the script can find the Tesseract executable whether it's
# running as a bundled .exe or a standard .py file.

# If the script is running as a bundled executable (.exe created by PyInstaller)
if getattr(sys, 'frozen', False):
    # The path is the directory of the executable itself.
    application_path = os.path.dirname(sys.executable)
# If the script is running as a standard .py file
else:
    # The path is the directory where the .py file is located.
    application_path = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the Tesseract executable, assuming it's in a 'tesseract' subfolder.
tesseract_path = os.path.join(application_path, 'tesseract', 'tesseract.exe')

# Point pytesseract to the Tesseract executable. This makes the script portable.
pytesseract.pytesseract.tesseract_cmd = tesseract_path
# --- END OF CONFIGURATION ---


print("Automation will start in 5 seconds...")
time.sleep(5)

try:
    # --- Step 1: Find and Fill the Input Fields ---
    print("Searching for the name label...")
    # Locate the 'isim_label.png' image on the screen to find our target window.
    isim_label_location = pyautogui.locateCenterOnScreen('isim_label.png', confidence=0.9)
    
    if isim_label_location:
        # First, click the label itself to ensure the target application window is active.
        pyautogui.click(isim_label_location)
        print("Clicked the 'Name:' label to activate the window.")
        time.sleep(0.3) # A brief pause for the window to come into focus.

        # Now, click on the text box, which is slightly below the label.
        pyautogui.click(isim_label_location.x, isim_label_location.y + 35)
        print("Clicked on the name input field.")
        time.sleep(0.5)

        # Use the copy-paste method for reliability with special characters.
        pyperclip.copy("Barış Kahraman")
        # Automatically select the correct paste shortcut (Ctrl+V for Windows, Cmd+V for Mac).
        pyautogui.hotkey('ctrl' if sys.platform == 'win32' else 'command', 'v')
        print("Name entered: Barış Kahraman")
    else:
        # If the initial label is not found, the script cannot proceed.
        print("ERROR: Could not find 'isim_label.png' on the screen.")
        sys.exit(1) # Exit with an error code.
    
    time.sleep(0.5)
    
    # Move focus to the next input field (Age).
    pyautogui.press('tab')
    time.sleep(0.5)
    
    # Enter the age using the same reliable copy-paste method.
    pyperclip.copy("35")
    pyautogui.hotkey('ctrl' if sys.platform == 'win32' else 'command', 'v')
    print("Age entered: 35")
    time.sleep(0.5)

    # --- Step 2: Activate the Save Button ---
    # Move focus from the Age field to the Save button.
    pyautogui.press('tab')
    time.sleep(0.5)
    # Activate the focused button using the space bar (more reliable than clicking).
    pyautogui.press('space')
    print("Save action activated!")
    time.sleep(1.5) # Wait for the confirmation dialog to appear.

    # --- Step 3: Read the Result from the Dialog Box ---
    print("Assuming the dialog box appears in the center of the screen...")
    # Get the screen dimensions to calculate the center.
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
    # Configure Tesseract to assume a single uniform block of text for better accuracy.
    custom_config = r'--oem 3 --psm 6'
    # Perform OCR on the screenshot using the Turkish language data.
    text = pytesseract.image_to_string(text_screenshot, lang="tur", config=custom_config)
    # Clean up the OCR result by removing extra whitespace and newlines.
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    # --- Step 4: Close the Dialog Box ---
    # Press Enter to click the default 'OK' button in the dialog.
    pyautogui.press('enter')
    print("\n🎉 Automation completed successfully! 🎉")
    sys.exit(0) # Exit with a success code.

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1) # Exit with an error code.
