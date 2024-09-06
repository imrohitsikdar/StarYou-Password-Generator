import tkinter as tk
from tkinter import ttk
import random
import string
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Password Generator")

# Input for password length
password_length_label = tk.Label(root, text="Password Length:")
password_length_label.pack()
password_length_spinbox = tk.Spinbox(root, from_=1, to=100)
password_length_spinbox.pack()

# Input for number of passwords
number_of_passwords_label = tk.Label(root, text="Number of Passwords:")
number_of_passwords_label.pack()
number_of_passwords_spinbox = tk.Spinbox(root, from_=1, to=100)
number_of_passwords_spinbox.pack()

# Generate Passwords button
generate_button = tk.Button(root, text="Generate Passwords")
generate_button.pack()

# Initialize passwords list
passwords = []

# Copy All Passwords button (initially disabled)
copy_all_button = tk.Button(root, text="Copy All Passwords", state=tk.DISABLED)
copy_all_button.pack()

# Frame to hold the passwords and scrollbar
passwords_frame = tk.Frame(root)
passwords_frame.pack(fill=tk.BOTH, expand=True)

# Canvas and scrollbar for scrolling through passwords
canvas = tk.Canvas(passwords_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(passwords_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Frame inside the canvas to hold password labels and buttons
passwords_list_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=passwords_list_frame, anchor="nw")

def generate_passwords():
    global passwords
    # Clear previous passwords
    for widget in passwords_list_frame.winfo_children():
        widget.destroy()

    try:
        length = int(password_length_spinbox.get())
        num_passwords = int(number_of_passwords_spinbox.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")
        return

    passwords = []
    for _ in range(num_passwords):
        password = ''.join(random.choices(
            string.ascii_letters + string.digits + string.punctuation, k=length))
        passwords.append(password)

    # Display passwords with individual copy buttons
    for idx, pwd in enumerate(passwords):
        pwd_label = tk.Label(passwords_list_frame, text=pwd)
        pwd_label.grid(row=idx, column=0, sticky='w', padx=5, pady=5)

        copy_button = tk.Button(passwords_list_frame, text="Copy", command=lambda p=pwd: copy_to_clipboard(p))
        copy_button.grid(row=idx, column=1, padx=5, pady=5)

    # Enable the "Copy All Passwords" button
    copy_all_button.config(state=tk.NORMAL)

    # Update the scroll region
    canvas.configure(scrollregion=canvas.bbox("all"))

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Password copied to clipboard.")

def copy_all_passwords(passwords):
    if not passwords:
        messagebox.showwarning("No passwords", "No passwords to copy.")
        return
    all_passwords = '\n'.join(passwords)
    root.clipboard_clear()
    root.clipboard_append(all_passwords)
    messagebox.showinfo("Copied", "All passwords copied to clipboard.")

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Bind mouse scroll to canvas
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Configure buttons
generate_button.config(command=generate_passwords)
copy_all_button.config(command=lambda: copy_all_passwords(passwords))

# Run the application
root.mainloop()
