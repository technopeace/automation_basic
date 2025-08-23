# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys
import traceback
import io

# --- UTF-8 OUTPUT FIX (Windows console safe) ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- NORMALIZATION FUNCTION (Turkish → Latin) ---
def normalize_text(text: str) -> str:
    mapping = str.maketrans("şŞıİçÇöÖüÜğĞ", "sSiIcCoOuUgG")
    return text.translate(mapping)

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

tesseract_path = os.path.join(application_path, "tesseract", "tesseract.exe")

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    print(f"ERROR: Tesseract not found at: {tesseract_path}")
    sys.exit(1)

print("Automation will start in 5 seconds...")
time.sleep(5)

try:
    print("Searching for the 'Name' label...")
    name_label_path = os.path.join(application_path, "isim_label.png")

    name_label_location = pyautogui.locateCenterOnScreen(
        name_label_path, confidence=0.3
    )

    if name_label_location:
        pyautogui.click(name_label_location)
        time.sleep(0.3)
        pyautogui.click(name_label_location.x, name_label_location.y + 35)

        name_value = "Barış Kahraman"
        pyperclip.copy(normalize_text(name_value))
        pyautogui.hotkey("ctrl", "v")
        print(f"Name entered: {normalize_text(name_value)}")
    else:
        print(f"ERROR: Could not find '{name_label_path}' on the screen.")
        sys.exit(1)

    time.sleep(0.5)
    pyautogui.press("tab")
    time.sleep(0.5)
    pyperclip.copy("35")
    pyautogui.hotkey("ctrl", "v")
    print("Age entered: 35")

    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.press("space")
    print("Save button activated!")
    time.sleep(1.2)

    print("Capturing dialog box...")
    screenWidth, screenHeight = pyautogui.size()
    dialog_region = (
        int((screenWidth - 400) / 2),
        int((screenHeight - 300) / 2) - 50,
        400,
        300,
    )
    text_screenshot = pyautogui.screenshot(region=dialog_region)

    # Only use English OCR
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(text_screenshot, lang="eng", config=custom_config)

    cleaned_text = normalize_text(" ".join(text.split()).strip())

    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    pyautogui.press("enter")
    print("Dialog closed with Enter.")

    # --- TEST CHECK ---
    expected = f"Kaydedildi! Isim: {normalize_text(name_value)} Yas: 35"
    if expected in cleaned_text:
        print("\n✅ TEST PASSED")
        sys.exit(0)
    else:
        print("\n❌ TEST FAILED: Expected text not found")
        sys.exit(1)

except Exception:
    print("An unexpected error occurred:")
    traceback.print_exc()
    sys.exit(1)
