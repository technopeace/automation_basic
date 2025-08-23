# app.py
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont # Font ayarları için import ediyoruz

def save_data():
    name = entry_name.get()
    age = entry_age.get()
    if name and age:
        messagebox.showinfo("Bilgi", f"Kaydedildi!\nİsim: {name}\nYaş: {age}")
    else:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")

# Pencere oluştur
root = tk.Tk()
root.title("İnşaat Asistanı - Demo")
root.geometry("300x250") # Pencereyi biraz büyüttük

# <<< DEĞİŞİKLİK BURADA: Daha büyük bir font tanımlıyoruz >>>
# Kalın ve büyük bir font oluşturuyoruz ki pyautogui rahatça bulabilsin.
buyuk_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

# Etiketler ve giriş alanları
# Etiketi oluştururken tanımladığımız büyük fontu kullanıyoruz.
tk.Label(root, text="İsim:", font=buyuk_font).pack(pady=10)
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Yaş:", font=buyuk_font).pack(pady=10)
entry_age = tk.Entry(root)
entry_age.pack()

# Buton
btn_save = tk.Button(root, text="Kaydet", command=save_data)
btn_save.pack(pady=20)

root.mainloop()
