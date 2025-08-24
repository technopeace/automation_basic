# -*- coding: utf-8 -*-
import sys
import io

# Python'un standart çıktı ve hata akışlarını UTF-8 kullanmaya zorla
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import traceback
import pygetwindow as gw

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
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

try:
    # --- Step 1: Hedef Pencereyi Bul ve Tam Ekran Yap ---
    target_title = "İnşaat Asistanı - Demo"
    print(f"Searching for window with title: '{target_title}'")
    app_window = gw.getWindowsWithTitle(target_title)

    if app_window:
        window = app_window[0]
        # --- DEĞİŞİKLİK BURADA: Pencereyi her zaman tam ekran yap ---
        print("Forcing window to the front and maximizing...")
        if window.isMinimized:
            window.restore()  # Önce simge durumundan çıkar
        
        window.maximize()     # Pencereyi tam ekran yap
        window.activate()     # Odağı pencereye ver
        
        print("Target window maximized and activated.")
        time.sleep(1.5)       # Tam ekran animasyonunun bitmesi için biraz bekle
    else:
        print(f"ERROR: Could not find window with title '{target_title}'")
        sys.exit(1)

    # --- Step 2: Fill Input Fields ---
    print("Searching for the 'Name' label...")
    name_label_path = os.path.join(application_path, "isim_label.png")
    name_label_location = pyautogui.locateCenterOnScreen(name_label_path, confidence=0.3)

    if name_label_location:
        # Etikete tıklamak yerine doğrudan giriş alanına tıkla
        pyautogui.click(name_label_location.x, name_label_location.y + 20)
        print("Clicked on name input field.")
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyperclip.copy("Baris Kahraman")
        pyautogui.hotkey("ctrl", "v")
        print("Name entered: Baris Kahraman")
    else:
        print(f"ERROR: Could not find '{name_label_path}'")
        pyautogui.screenshot(os.path.join(application_path, "error_screenshot_label_not_found.png"))
        sys.exit(1)

    time.sleep(0.5)
    pyautogui.press("tab")
    time.sleep(0.5)

    pyperclip.copy("35")
    pyautogui.hotkey("ctrl", "v")
    print("Age entered: 35")
    time.sleep(0.5)

    # --- Step 3: Activate Save Button ---
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.press("space")
    print("Save button activated!")
    time.sleep(1.5)

    # --- Step 4: Capture Dialog Box and OCR ---
    print("Capturing full screen...")
    full_screenshot = pyautogui.screenshot()
    full_screenshot_path = os.path.join(application_path, "full-screenshot.png")
    full_screenshot.save(full_screenshot_path)
    print(f"Full screen debug screenshot saved: {full_screenshot_path}")

    print("Capturing dialog box...")
    screenWidth, screenHeight = pyautogui.size()
    dialog_width = 400
    dialog_height = 300
    dialog_x = int((screenWidth - dialog_width) / 2)
    dialog_y = int((screenHeight - dialog_height) / 2) - 50
    dialog_region = (dialog_x, dialog_y, dialog_width, dialog_height)
    text_screenshot = pyautogui.screenshot(region=dialog_region)
    screenshot_path = os.path.join(application_path, "ocr-screenshot.png")
    text_screenshot.save(screenshot_path)
    print(f"OCR debug screenshot saved: {screenshot_path}")

    custom_config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(text_screenshot, lang="eng", config=custom_config)
    cleaned_text = " ".join(text.split()).strip()
    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    pyautogui.press("enter")
    print("Dialog closed with Enter.")

    # --- Step 5: Final Success Message ---
    print("\nAutomation completed successfully!")
    sys.exit(0)

except Exception as e:
    print("An unexpected error occurred:")
    traceback.print_exc()
    sys.exit(1)