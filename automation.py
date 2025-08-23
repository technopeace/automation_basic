# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys
import pandas as pd # Required for parsing OCR data

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
# This block ensures the script can find the Tesseract executable whether it's
# running as a bundled .exe or a standard .py file.
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

tesseract_path = os.path.join(application_path, 'tesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path
# --- END OF CONFIGURATION ---

print("Automation will start in 5 seconds...")
time.sleep(5)

try:
    # --- Step 1: Find the Target Window using OCR and Fill Inputs ---
    print("Searching for the 'İsim:' label using OCR...")
    
    # --- NEW: RESILIENT OCR-BASED FINDING LOOP ---
    # Try to find the text on the screen for up to 15 seconds before giving up.
    start_time = time.time()
    isim_label_location = None
    while time.time() - start_time < 15:
        # Take a screenshot of the entire screen
        screenshot = pyautogui.screenshot()
        
        # Use Tesseract to get detailed data about all text on the screen
        # output_type=pytesseract.Output.DATAFRAME makes it easy to parse with pandas
        ocr_data = pytesseract.image_to_data(screenshot, lang='tur', output_type=pytesseract.Output.DATAFRAME)
        
        # Filter out words with low confidence to avoid false positives
        ocr_data = ocr_data[ocr_data.conf > 60]
        
        # Search for the specific label text "İsim:"
        # We use .str.contains() to be flexible with potential OCR errors
        label_df = ocr_data[ocr_data['text'].str.contains('İsim', na=False)]
        
        if not label_df.empty:
            # If found, get the coordinates from the first match
            label_row = label_df.iloc[0]
            
            # Calculate the center coordinates of the found text
            x = label_row['left'] + (label_row['width'] / 2)
            y = label_row['top'] + (label_row['height'] / 2)
            
            isim_label_location = (x, y)
            print(f"Label 'İsim:' found via OCR at ({int(x)}, {int(y)})!")
            break
            
        print("Label not found, retrying in 1 second...")
        time.sleep(1)
    # --- END OF NEW LOOP ---

    if isim_label_location:
        # The rest of the automation logic proceeds as before
        pyautogui.click(isim_label_location)
        time.sleep(0.3)
        # Click slightly below the found label to target the input box
        pyautogui.click(isim_label_location[0], isim_label_location[1] + 35)
        time.sleep(0.5)
        pyperclip.copy("Barış Kahraman")
        # Automatically select the correct paste shortcut for the OS
        pyautogui.hotkey('ctrl' if sys.platform == 'win32' else 'command', 'v')
        print("Name entered: Barış Kahraman")
    else:
        print("ERROR: Could not find 'İsim:' label on the screen after 15 seconds.")
        sys.exit(1)
    
    time.sleep(0.5)
    pyautogui.press('tab')
    time.sleep(0.5)
    pyperclip.copy("35")
    pyautogui.hotkey('ctrl' if sys.platform == 'win32' else 'command', 'v')
    print("Age entered: 35")
    time.sleep(0.5)

    # --- Step 2: Activate the Save Button ---
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('space')
    print("Save action activated!")
    time.sleep(1.5)

    # --- Step 3: Read the Result from the Dialog Box ---
    print("Assuming the dialog box appears in the center of the screen...")
    screenWidth, screenHeight = pyautogui.size()
    dialog_region = (int(screenWidth/2 - 200), int(screenHeight/2 - 150 - 50), 400, 300)
    text_screenshot = pyautogui.screenshot(region=dialog_region)
    
    print("Sending screenshot to Tesseract for OCR...")
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(text_screenshot, lang="tur", config=custom_config)
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    # --- Step 4: Close the Dialog Box ---
    pyautogui.press('enter')
    print("\n🎉 Automation completed successfully! 🎉")
    sys.exit(0)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
