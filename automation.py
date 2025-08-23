# automation.py
import pyautogui
import pytesseract
from PIL import Image
import time
import pyperclip
import os
import sys
import traceback  # <-- Import the traceback module to get detailed errors

# --- DYNAMIC TESSERACT PATH CONFIGURATION ---
# Bu blok, script'in .exe veya .py olarak çalışmasına bakmaksızın
# kendi bulunduğu klasörün yolunu bulmasını sağlar.
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Tesseract'in tam yolunu, ana programın yanındaki 'tesseract' klasörüne göre oluşturur.
tesseract_path = os.path.join(application_path, "tesseract", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path
# --- END OF CONFIGURATION ---


print("Automation will start in 5 seconds...")
time.sleep(5)

try:
    # --- Step 1: Find and Fill the Input Fields ---
    print("Searching for the name label...")

    # <<< DEĞİŞİKLİK BURADA: Resim dosyasının tam yolunu oluşturuyoruz >>>
    # Bu, script'in nereden çalıştırıldığından bağımsız olarak resmin bulunmasını garantiler.
    isim_label_path = os.path.join(application_path, "isim_label.png")

    # pyautogui'ye, resmi bu tam yolu kullanarak aramasını söylüyoruz.
    isim_label_location = pyautogui.locateCenterOnScreen(
        isim_label_path, confidence=0.4
    )

    if isim_label_location:
        # Pencereyi aktif etmek için önce etiketin kendisine tıkla.
        pyautogui.click(isim_label_location)
        print("Clicked the 'Name:' label to activate the window.")
        time.sleep(0.3)  # Pencerenin öne gelmesi için kısa bir bekleme.

        # Şimdi metin kutusuna tıkla.
        pyautogui.click(isim_label_location.x, isim_label_location.y + 35)
        print("Clicked on the name input field.")
        time.sleep(0.5)

        # Türkçe karakterlerle güvenilir şekilde çalışmak için kopyala-yapıştır yöntemi.
        pyperclip.copy("Barış Kahraman")
        # İşletim sistemine göre doğru yapıştırma kısayolunu otomatik seçer.
        pyautogui.hotkey("ctrl" if sys.platform == "win32" else "command", "v")
        print("Name entered: Barış Kahraman")
    else:
        # Eğer etiket bulunamazsa, script devam edemez.
        print(f"ERROR: Could not find '{isim_label_path}' on the screen.")
        sys.exit(1)  # Hata koduyla çık.

    time.sleep(0.5)

    # Bir sonraki alana (Yaş) odaklan.
    pyautogui.press("tab")
    time.sleep(0.5)

    # Yaşı aynı güvenilir kopyala-yapıştır yöntemiyle gir.
    pyperclip.copy("35")
    pyautogui.hotkey("ctrl" if sys.platform == "win32" else "command", "v")
    print("Age entered: 35")
    time.sleep(0.5)

    # --- Step 2: Activate the Save Button ---
    # Yaş alanından Kaydet butonuna odaklan.
    pyautogui.press("tab")
    time.sleep(0.5)
    # Odaklanılan butonu boşluk tuşuyla aktive et (tıklamaktan daha güvenilir).
    pyautogui.press("space")
    print("Save action activated!")
    time.sleep(1.5)  # Onay diyalogunun belirmesi için bekle.

    # --- Step 3: Read the Result from the Dialog Box ---
    print("Assuming the dialog box appears in the center of the screen...")
    # Ekran boyutlarını alıp merkezi hesapla.
    screenWidth, screenHeight = pyautogui.size()

    # Ekranın merkezinde diyalogun beklendiği bir bölge tanımla.
    dialog_width = 400
    dialog_height = 300
    dialog_x = int((screenWidth - dialog_width) / 2)
    # Diyalogu daha iyi yakalamak için Y koordinatını biraz yukarı kaydırıyoruz.
    dialog_y = int((screenHeight - dialog_height) / 2) - 50
    dialog_region = (dialog_x, dialog_y, dialog_width, dialog_height)

    # Sadece o bölgenin ekran görüntüsünü al.
    text_screenshot = pyautogui.screenshot(region=dialog_region)

    print("Sending screenshot to Tesseract for OCR...")
    # Tesseract'i tek bir metin bloğu varsayacak şekilde yapılandırarak doğruluğu artır.
    custom_config = r"--oem 3 --psm 6"
    # Ekran görüntüsünde Türkçe dil verisini kullanarak OCR işlemi yap.
    text = pytesseract.image_to_string(
        text_screenshot, lang="tur", config=custom_config
    )
    # OCR sonucunu ekstra boşluk ve satır atlamalarından temizle.
    cleaned_text = " ".join(text.split()).strip()

    print("-" * 30)
    print(f"Text read from dialog: '{cleaned_text}'")
    print("-" * 30)

    # --- Step 4: Close the Dialog Box ---
    # Diyalogdaki varsayılan 'OK' butonuna tıklamak için Enter'a bas.
    pyautogui.press("enter")
    print("\n🎉 Automation completed successfully! 🎉")
    sys.exit(0)  # Başarı koduyla çık.

except Exception as e:
    # --- NEW: DETAILED ERROR REPORTING ---
    # This will print the full technical error details (traceback)
    # to help us understand the root cause of the crash.
    print(f"An unexpected error occurred:")
    traceback.print_exc()
    sys.exit(1)  # Hata koduyla çık.
