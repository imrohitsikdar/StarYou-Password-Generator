import secrets
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Function to generate a secure random password
def generate_password(length):
    if length < 4:
        return "Password length must be at least 4 to include all character categories."

    # Ensure password includes at least one lowercase, uppercase, number, and symbol
    all_categories = (
        secrets.choice(string.ascii_lowercase) +
        secrets.choice(string.ascii_uppercase) +
        secrets.choice(string.digits) +
        secrets.choice(string.punctuation)
    )

    # Fill the rest of the password length with a mix of all categories
    remaining_length = length - 4
    mixed_chars = string.ascii_letters + string.digits + string.punctuation
    all_categories += ''.join(secrets.choice(mixed_chars) for _ in range(remaining_length))

    # Shuffle the password to make it unpredictable
    password = ''.join(secrets.choice(all_categories) for _ in range(len(all_categories)))
    return password

# Function to generate multiple passwords
def generate_passwords(event=None):
    try:
        length = int(length_entry.get())
        count = int(count_entry.get())

        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4 characters.")
            return

        # Clear previous results and repack password_canvas
        for widget in result_frame.winfo_children():
            widget.destroy()  # Clear the result frame

        # Generate passwords
        passwords = [generate_password(length) for _ in range(count)]

        # Add headers for the Excel-like grid
        ttk.Label(result_frame, text="Serial No.", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(result_frame, text="Password", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(result_frame, text="Copy", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

        # Add each password with serial number and copy button
        for i, pwd in enumerate(passwords, start=1):
            ttk.Label(result_frame, text=str(i), font=("Arial", 10)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(result_frame, text=pwd, font=("Arial", 10)).grid(row=i, column=1, padx=5, pady=5, sticky="w")

            # Copy button for each password
            copy_button = ttk.Button(result_frame, text="Copy", command=lambda pwd=pwd: copy_password(pwd))
            copy_button.grid(row=i, column=2, padx=5, pady=5)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for length and count.")

# Function to copy a single password from the results
def copy_password(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Copied", f"Password copied to clipboard: {password}")

# Function to copy all passwords to the clipboard
def copy_all_passwords():
    passwords = "\n".join(password_label.cget("text") for password_label in result_frame.winfo_children() if isinstance(password_label, ttk.Label))
    root.clipboard_clear()
    root.clipboard_append(passwords)
    messagebox.showinfo("Copied", "All passwords copied to clipboard.")

# Function to clear all fields
def clear_fields(event=None):
    length_entry.delete(0, tk.END)
    count_entry.delete(0, tk.END)
    for widget in result_frame.winfo_children():
        widget.destroy()  # Clear the result frame

# Function to handle mouse wheel scrolling
def on_mouse_wheel(event):
    if event.delta != 0:  # For Windows
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    else:  # For Mac/Linux
        canvas.yview_scroll(-1 if event.num == 5 else 1, "units")

# Function to cycle through fields with arrow keys
def focus_next(event):
    # Check which entry field is currently focused
    if event.keysym == 'Down':
        if root.focus_get() == length_entry:
            count_entry.focus_set()  # Move focus to the 'Number of Passwords' entry
        elif root.focus_get() == count_entry:
            length_entry.focus_set()  # Move focus back to the 'Password Length' entry

    elif event.keysym == 'Up':
        if root.focus_get() == count_entry:
            length_entry.focus_set()  # Move focus to the 'Password Length' entry
        elif root.focus_get() == length_entry:
            count_entry.focus_set()  # Move focus back to the 'Number of Passwords' entry

# Create the main window
root = tk.Tk()
root.title("StarYou Password Generator")
root.geometry("600x400")
root.minsize(400, 300)

# Heading label
heading_label = ttk.Label(root, text="StarYou Password Generator", font=("Arial", 16, "bold"))
heading_label.pack(pady=10)

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Length input
length_label = ttk.Label(input_frame, text="Password Length:")
length_label.grid(row=0, column=0, padx=5, pady=5)
length_entry = ttk.Entry(input_frame, width=10)
length_entry.grid(row=0, column=1, padx=5, pady=5)

# Count input
count_label = ttk.Label(input_frame, text="Number of Passwords:")
count_label.grid(row=1, column=0, padx=5, pady=5)
count_entry = ttk.Entry(input_frame, width=10)
count_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons frame
buttons_frame = ttk.Frame(root)
buttons_frame.pack(pady=10)

# Generate button
generate_button = ttk.Button(buttons_frame, text="Generate Passwords", command=generate_passwords)
generate_button.grid(row=0, column=0, padx=5, pady=5)

# Clear button
clear_button = ttk.Button(buttons_frame, text="Clear", command=clear_fields)
clear_button.grid(row=0, column=1, padx=5, pady=5)

# Copy All button (placed in the buttons frame)
copy_all_button = ttk.Button(buttons_frame, text="Copy All Passwords", command=copy_all_passwords)
copy_all_button.grid(row=0, column=2, padx=5, pady=5)

# Create a canvas widget for scrolling
canvas_frame = ttk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add a scrollbar to the canvas
canvas = tk.Canvas(canvas_frame)
scrollbar_y = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar_x = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas to hold password results
result_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=result_frame, anchor="nw")

# Update the scrollable region whenever the window is resized
result_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Bind mouse wheel for vertical scrolling
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Bind Enter and Delete keys
root.bind("<Return>", generate_passwords)  # Bind Enter key to generate passwords
root.bind("<Delete>", clear_fields)  # Bind Delete key to clear fields

# Bind Arrow keys to switch focus between fields
root.bind("<Down>", focus_next)  # Bind Down arrow key to cycle between fields
root.bind("<Up>", focus_next)    # Bind Up arrow key to cycle between fields

# Run the application
root.mainloop()
