# automation_fast.py
import pyautogui
import pytesseract
from PIL import Image
import time, pyperclip, os, sys, traceback

# --- PATH CONFIGURATION ---
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

tesseract_path = os.path.join(application_path, "tesseract", "tesseract.exe")
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    print(f"ERROR: Tesseract not found at {tesseract_path}")
    sys.exit(1)

print("Automation will start in 5 seconds...")
time.sleep(5)

def safe_locate(img_path, confidence=0.9, region=None, timeout=10):
    """Locate image on screen with timeout to prevent infinite scanning."""
    start = time.time()
    while time.time() - start < timeout:
        loc = pyautogui.locateCenterOnScreen(img_path, confidence=confidence, region=region)
        if loc:
            return loc
        time.sleep(0.5)
    return None

try:
    # --- Step 1: Find and Fill the Input Fields ---
    print("Searching for the 'Name' label...")
    name_label_path = os.path.join(application_path, "isim_label.png")

    # Restrict search to top-left quarter of the screen for speed
    sw, sh = pyautogui.size()
    name_region = (0, 0, sw//2, sh//2)

    name_label_location = safe_locate(name_label_path, confidence=0.9, region=name_region)

    if name_label_location:
        pyautogui.click(name_label_location)
        print("Clicked the 'Name:' label to activate window.")
        time.sleep(0.3)
        pyautogui.click(name_label_location.x, name_label_location.y + 35)
        print("Clicked on name input field.")
        pyperclip.copy("John Doe")
        pyautogui.hotkey("ctrl", "v")
        print("Name entered: John Doe")
    else:
        print(f"ERROR: Could not find '{name_label_path}' on the screen.")
        sys.exit(1)

    time.sleep(0.5)
    pyautogui.press("tab"); time.sleep(0.5)
    pyperclip.copy("35"); pyautogui.hotkey("ctrl", "v")
    print("Age entered: 35")

    # --- Step 2: Activate Save Button ---
    pyautogui.press("tab"); time.sleep(0.5)
    pyautogui.press("space")
    print("Save button activated!")
    time.sleep(1.5)

    # --- Step 3: Read Dialog Box ---
    print("Capturing dialog box...")
    dialog_w, dialog_h = 400, 200
    dialog_x, dialog_y = (sw - dialog_w)//2, (sh - dialog_h)//2
    dialog_region = (dialog_x, dialog_y, dialog_w, dialog_h)

    text_img = pyautogui.screenshot(region=dialog_region)
    text = pytesseract.image_to_string(text_img, lang="eng", config="--oem 3 --psm 6")
    cleaned = " ".join(text.split()).strip()
    print("-" * 30)
    print(f"Text read from dialog: '{cleaned}'")
    print("-" * 30)

    # --- Step 4: Close Dialog ---
    print("Searching for OK button...")
    ok_button_path = os.path.join(application_path, "ok_button.png")
    ok_region = (dialog_x, dialog_y, dialog_w, dialog_h)

    ok_button_location = safe_locate(ok_button_path, confidence=0.9, region=ok_region)

    if ok_button_location:
        pyautogui.click(ok_button_location)
        print("Clicked OK button.")
    else:
        print("OK button not found, pressing Enter instead.")
        pyautogui.press("enter")

    print("\n🎉 Automation completed successfully! 🎉")
    sys.exit(0)

except Exception:
    print("An unexpected error occurred:")
    traceback.print_exc()
    sys.exit(1)
