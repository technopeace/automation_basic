# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip

# <<< YENİ SATIRI BURAYA EKLEYİN >>>
# macOS'te Homebrew ile kurulan Tesseract'in yolunu belirtiyoruz
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
# --- Kurulum ve Bilgilendirme ---
# macOS'te Homebrew ile Tesseract kurduysanız bu satırı kullanmanız gerekebilir:
# pytesseract.pytesseract.tesseract_cmd = r'/opt_homebrew/bin/tesseract'

print("UYARI: Bu scriptin çalışması için 'isim_label.png' dosyasını oluşturmanız gerekir.")
print("-" * 30)
print("5 saniye içinde otomasyon başlayacak. Lütfen 'İnşaat Asistanı' uygulamasını açın ve öne getirin.")
time.sleep(5)

try:


    # Türkçe karakterler için kopyala-yapıştır yöntemi
    pyautogui.press('tab')
    pyperclip.copy("Barış Kahraman")
    pyautogui.hotkey('command', 'v')
    
    print("İsim yazıldı: Barış Kahraman")
    
    pyautogui.press('tab')
    time.sleep(0.5)
    
    pyperclip.copy("35")
    pyautogui.hotkey('command', 'v')
    print("Yaş yazıldı: 35")
    time.sleep(0.5)

    # --- Adım 3: Kaydetme İşlemini Aktive Etme ---
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('space')
    print("Kaydetme işlemi aktive edildi!")
    time.sleep(1.5)

    # --- Adım 4: Ekranın Merkezindeki Diyalog Kutusunu Oku ---
    print("Diyalog kutusunun ekran merkezinde olduğu varsayılıyor...")
    
    screenWidth, screenHeight = pyautogui.size()
    
    dialog_width = 400
    dialog_height = 300
    dialog_x = int((screenWidth - dialog_width) / 2)
    dialog_y = int((screenHeight - dialog_height) / 2) - 50
    
    dialog_region = (dialog_x, dialog_y, dialog_width, dialog_height)
    
    text_screenshot = pyautogui.screenshot(region=dialog_region)
    screenshot_path = "dialog_screenshot.png"
    text_screenshot.save(screenshot_path)
    print(f"Ekranın merkezindeki '{screenshot_path}' dosyası kaydedildi.")
    
    print("Görüntü işlenmeden, ham haliyle Tesseract'e gönderiliyor...")
    
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(text_screenshot, lang="tur", config=custom_config)
    
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Diyalogdan Okunan Yazı: '{cleaned_text}'")
    print("-" * 30)

    # --- Adım 5: Diyalog Kutusunu Kapatma ---
    print("Diyalog kutusu 'Enter' tuşuna basılarak kapatılıyor...")
    time.sleep(1)
    pyautogui.press('enter') # 'OK' butonu için Enter tuşuna bas
    
    print("\n🎉 Otomasyon başarıyla tamamlandı! 🎉")


except Exception as e:
    print(f"Beklenmedik bir hata oluştu: {e}")