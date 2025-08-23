# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys
import traceback  # For detailed error logging

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
if getattr(sys, "frozen", False):
    # Running as a bundled exe
    application_path = os.path.dirname(sys.executable)
else:
    # Running as a normal .py script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Path to Tesseract executable
tesseract_path = os.path.join(application_path, "tesseract", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Path to tessdata directory
tessdata_dir_path = os.path.join(application_path, "tesseract", "tessdata")

# --- LANGUAGE CHECK ---
tur_path = os.path.join(tessdata_dir_path, "tur.traineddata")
if os.path.exists(tur_path):
    ocr_lang = "tur"
    print("✅ Turkish language data found, using 'tur'.")
else:
    ocr_lang = "eng"
    print("⚠️ 'tur.traineddata' not found, falling back to English (eng).")

print("Automation will start in 5 seconds...")
time.sleep(5)

try:
    # --- Step 1: Find and Fill the Input Fields ---
    print("Searching for the name label...")

    isim_label_path = os.path.join(application_path, "isim_label.png")
    isim_label_location = pyautogui.locateCenterOnScreen(isim_label_path, confidence=0.4)

    if isim_label_location:
        # Click the label to activate the window
        pyautogui.click(isim_label_location)
        print("Clicked the 'Name:' label to activate the window.")
        time.sleep(0.3)

        # Click input field
        pyautogui.click(isim_label_location.x, isim_label_location.y + 35)
        print("Clicked on the name input field.")
        time.sleep(0.5)

        # Paste name
        pyperclip.copy("Barış Kahraman")
        pyautogui.hotkey("ctrl" if sys.platform == "win32" else "command", "v")
        print("Name entered: Baris Kahraman")
    else:
        print(f"❌ Could not find '{isim_label_path}' on the screen.")
        sys.exit(1)

    time.sleep(0.5)

    # Move to Age field
    pyautogui.press("tab")
    time.sleep(0.5)

    # Enter age
    pyperclip.copy("35")
    pyautogui.hotkey("ctrl" if sys.platform == "win32" else "command", "v")
    print("Age entered: 35")
    time.sleep(0.5)

    # --- Step 2: Save action ---
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.press("space")
    print("Save action activated!")
    time.sleep(1.5)

    # --- Step 3: OCR on dialog ---
    print("Assuming the dialog box appears in the center of the screen...")
    screenWidth, screenHeight = pyautogui.size()
    dialog_width, dialog_height = 400, 300
    dialog_x = int((screenWidth - dialog_width) / 2)
    dialog_y = int((screenHeight - dialog_height) / 2) - 50
    dialog_region = (dialog_x, dialog_y, dialog_width, dialog_height)

    text_screenshot = pyautogui.screenshot(region=dialog_region)

    print("Sending screenshot to Tesseract for OCR...")
    custom_config = f'--oem 3 --psm 6 --tessdata-dir {tessdata_dir_path}'

    text = pytesseract.image_to_string(
        text_screenshot, lang=ocr_lang, config=custom_config
    )
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    # Close dialog
    pyautogui.press("enter")
    print("\n🎉 Automation completed successfully!")
    sys.exit(0)

except Exception as e:
    print("❌ An unexpected error occurred:")
    traceback.print_exc()
    sys.exit(1)
