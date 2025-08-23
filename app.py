# app.py
import tkinter as tk
from tkinter import messagebox

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
root.geometry("300x200")

# Etiketler ve giriş alanları
tk.Label(root, text="İsim:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Yaş:").pack(pady=5)
entry_age = tk.Entry(root)
entry_age.pack()

# Buton
btn_save = tk.Button(root, text="Kaydet", command=save_data)
btn_save.pack(pady=20)

root.mainloop()
