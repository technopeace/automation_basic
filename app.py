# app.py
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from core_logic import process_user_data  # <-- IMPORT the shared logic

def show_custom_info(title, message):
    """
    Displays a custom info box with the specified title and message.
    """
    dialog_root = tk.Toplevel()
    dialog_root.title(title)
    dialog_root.transient(root)

    default_font = tkFont.nametofont("TkDefaultFont")
    custom_font = tkFont.Font(
        family=default_font.cget("family"),
        size=default_font.cget("size") * 2,
        weight="bold"
    )

    message_label = tk.Label(
        dialog_root,
        text=message,
        font=custom_font,
        padx=25,
        pady=25
    )
    message_label.pack()

    ok_button = tk.Button(
        dialog_root,
        text="OK",
        command=dialog_root.destroy,
        width=10,
        pady=5
    )
    ok_button.pack(pady=(0, 20))

    dialog_root.update_idletasks()
    window_width = dialog_root.winfo_width()
    window_height = dialog_root.winfo_height()
    screen_width = dialog_root.winfo_screenwidth()
    screen_height = dialog_root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    dialog_root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    dialog_root.wait_window()


def save_data():
    """
    Gets data from entry fields, passes it to the core logic,
    and displays the result in the GUI.
    """
    name = entry_name.get()
    age = entry_age.get()
    
    # Call the shared logic function
    result_message = process_user_data(name, age)
    
    if result_message:
        # If logic was successful, show the custom message box
        show_custom_info("Information", result_message)
        # Also print to console for PyAutoGUI test to see
        # We replace newline with a space to match the test's expected output format
        print(result_message.replace("\n", " "))
    else:
        # If logic returned an error, show a warning
        messagebox.showwarning("Warning", "Please fill in all fields!")

# --- Main Application Window ---
root = tk.Tk()
root.title("Construction Assistant - Demo")
root.geometry("300x250")

large_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

tk.Label(root, text="Name:", font=large_font).pack(pady=10)
entry_name = tk.Entry(root, font=large_font)
entry_name.pack()

tk.Label(root, text="Age:", font=large_font).pack(pady=10)
entry_age = tk.Entry(root, font=large_font)
entry_age.pack()

btn_save = tk.Button(root, text="Save", command=save_data, font=large_font)
btn_save.pack(pady=20)

root.mainloop()
