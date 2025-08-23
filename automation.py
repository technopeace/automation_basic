# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip

# <<< YENi SATIRI BURAYA EKLEYiN >>>
# macOS'te Homebrew ile kurulan Tesseract'in yolunu belirtiyoruz
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
# --- Kurulum ve Bilgilendirme ---
# macOS'te Homebrew ile Tesseract kurduysaniz bu satiri kullanmaniz gerekebilir:
# pytesseract.pytesseract.tesseract_cmd = r'/opt_homebrew/bin/tesseract'

print("UYARI: Bu scriptin calismasi icin 'isim_label.png' dosyasini olusturmaniz gerekir.")
print("-" * 30)
print("5 saniye icinde otomasyon baslayacak. Lutfen 'insaat Asistani' uygulamasini acin ve one getirin.")
time.sleep(5)

try:


    # Turkce karakterler icin kopyala-yapistir yontemi
    pyautogui.press('tab')
    pyperclip.copy("Baris Kahraman")
    pyautogui.hotkey('command', 'v')
    
    print("isim yazildi: Baris Kahraman")
    
    pyautogui.press('tab')
    time.sleep(0.5)
    
    pyperclip.copy("35")
    pyautogui.hotkey('command', 'v')
    print("Yas yazildi: 35")
    time.sleep(0.5)

    # --- Adim 3: Kaydetme islemini Aktive Etme ---
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('space')
    print("Kaydetme islemi aktive edildi!")
    time.sleep(1.5)

    # --- Adim 4: Ekranin Merkezindeki Diyalog Kutusunu Oku ---
    print("Diyalog kutusunun ekran merkezinde oldugu varsayiliyor...")
    
    screenWidth, screenHeight = pyautogui.size()
    
    dialog_width = 400
    dialog_height = 300
    dialog_x = int((screenWidth - dialog_width) / 2)
    dialog_y = int((screenHeight - dialog_height) / 2) - 50
    
    dialog_region = (dialog_x, dialog_y, dialog_width, dialog_height)
    
    text_screenshot = pyautogui.screenshot(region=dialog_region)
    screenshot_path = "dialog_screenshot.png"
    text_screenshot.save(screenshot_path)
    print(f"Ekranin merkezindeki '{screenshot_path}' dosyasi kaydedildi.")
    
    print("Goruntu islenmeden, ham haliyle Tesseract'e gonderiliyor...")
    
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(text_screenshot, lang="tur", config=custom_config)
    
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Diyalogdan Okunan Yazi: '{cleaned_text}'")
    print("-" * 30)

    # --- Adim 5: Diyalog Kutusunu Kapatma ---
    print("Diyalog kutusu 'Enter' tusuna basilarak kapatiliyor...")
    time.sleep(1)
    pyautogui.press('enter') # 'OK' butonu icin Enter tusuna bas
    
    print("\n🎉 Otomasyon basariyla tamamlandi! 🎉")


except Exception as e:
    print(f"Beklenmedik bir hata olustu: {e}")