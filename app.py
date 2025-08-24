# app.py
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

def show_custom_info(title, message):
    """
    Displays a custom info box with the specified title and message.
    The text will be bold and twice the size of the default font.
    """
    # Create and hide the main window for the dialog
    # This makes the dialog modal
    dialog_root = tk.Toplevel()
    dialog_root.title(title)
    dialog_root.transient(root) # Keep it on top of the main window

    # Get the default font, then create a new, larger, bold font
    default_font = tkFont.nametofont("TkDefaultFont")
    custom_font = tkFont.Font(
        family=default_font.cget("family"),
        size=default_font.cget("size") * 2, # Double the size
        weight="bold" # Make it bold
    )

    # Create a Label to display the message with the custom font
    message_label = tk.Label(
        dialog_root,
        text=message,
        font=custom_font,
        padx=25,
        pady=25
    )
    message_label.pack()

    # Add an "OK" button to close the dialog
    ok_button = tk.Button(
        dialog_root,
        text="OK",
        command=dialog_root.destroy,
        width=10,
        pady=5
    )
    ok_button.pack(pady=(0, 20))

    # Center the dialog on the screen
    dialog_root.update_idletasks()
    window_width = dialog_root.winfo_width()
    window_height = dialog_root.winfo_height()
    screen_width = dialog_root.winfo_screenwidth()
    screen_height = dialog_root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    dialog_root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Wait until the user closes the dialog
    dialog_root.wait_window()


def save_data():
    """
    Gets data from entry fields and shows a custom success message
    or a standard warning message.
    """
    name = entry_name.get()
    age = entry_age.get()
    if name and age:
        # <<< CHANGE HERE: Call the new custom message box function >>>
        info_message = f"Saved!\nName: {name}\nAge: {age}"
        show_custom_info("Information", info_message)
    else:
        # The warning message can remain standard
        messagebox.showwarning("Warning", "Please fill in all fields!")

# --- Main Application Window ---

# Create the main window
root = tk.Tk()
root.title("Construction Assistant - Demo")
root.geometry("300x250")

# Define a large font for labels
large_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

# Create and place widgets (Labels, Entry fields, Button)
tk.Label(root, text="Name:", font=large_font).pack(pady=10)
entry_name = tk.Entry(root, font=large_font)
entry_name.pack()

tk.Label(root, text="Age:", font=large_font).pack(pady=10)
entry_age = tk.Entry(root, font=large_font)
entry_age.pack()

btn_save = tk.Button(root, text="Save", command=save_data, font=large_font)
btn_save.pack(pady=20)

# Start the main event loop
root.mainloop()
