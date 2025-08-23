# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys
# pandas is no longer needed

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
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
    # --- Step 1: Find the Target Window using Image Recognition and Fill Inputs ---
    print("Searching for the name label image ('isim_label.png')...")
    
    # --- NEW: RESILIENT AND FAST IMAGE-BASED FINDING LOOP ---
    # Try to find the image for up to 10 seconds before giving up.
    # This is much faster than full-screen OCR.
    start_time = time.time()
    isim_label_location = None
    while time.time() - start_time < 10:
        # Use locateCenterOnScreen which is highly optimized for this task.
        isim_label_location = pyautogui.locateCenterOnScreen('isim_label.png', confidence=0.8)
        if isim_label_location:
            print("Name label found!")
            break
        print("Label not found, retrying...")
        time.sleep(0.5) # Wait half a second before trying again.
    # --- END OF NEW LOOP ---

    if isim_label_location:
        # The rest of the automation logic proceeds as before
        pyautogui.click(isim_label_location)
        time.sleep(0.3)
        pyautogui.click(isim_label_location[0], isim_label_location[1] + 35)
        time.sleep(0.5)
        pyperclip.copy("Barış Kahraman")
        pyautogui.hotkey('ctrl' if sys.platform == 'win32' else 'command', 'v')
        print("Name entered: Barış Kahraman")
    else:
        print("ERROR: Could not find 'isim_label.png' on the screen after 10 seconds.")
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
