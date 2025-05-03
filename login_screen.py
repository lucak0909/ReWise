import tkinter as tk
from tkinter import messagebox
import subprocess
import csv
import os

USER_FILE = "users.csv"

# Ensure users.csv exists with correct headers
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        # Columns: username, password, balance, rate, user_type, child_username
        writer.writerow(["username", "password", "balance", "rate", "user_type", "child_username"])


def open_dashboard(username, user_type):
    app.destroy()
    if user_type == "parent":
        subprocess.run(["python", "dashboard_screen.py", username, user_type])
    else:
        subprocess.run(["python", "quiz_screen.py", username])


def login(event=None):  # event optional for Enter key
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == username and row[1] == password:
                open_dashboard(username, row[4])  # pass user_type
                return

    messagebox.showerror("Login Failed", "Invalid username or password.")


def signup():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    user_type = user_type_var.get()
    child_username = child_entry.get().strip() if user_type == "parent" else ""

    if not username or not password:
        messagebox.showwarning("Missing Info", "Both username and password are required.")
        return
    if user_type == "parent" and not child_username:
        messagebox.showwarning("Missing Info", "Please enter the child's username.")
        return

    # Check for existing username
    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == username:
                messagebox.showerror("Error", "Username already exists.")
                return

    # Append new user
    with open(USER_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        # New users start with balance 0, rate 0
        writer.writerow([username, password, "0", "0", user_type, child_username])

    messagebox.showinfo("Success", f"{user_type.capitalize()} account created! Logging you in...")
    open_dashboard(username, user_type)


# GUI Setup
app = tk.Tk()
app.title("ReWise Login")
app.geometry("375x667")

# Title
tk.Label(app, text="ReWise", font=("Helvetica", 24)).pack(pady=40)

# Username
tk.Label(app, text="Username").pack()
username_entry = tk.Entry(app)
username_entry.pack(pady=5)

# Password
tk.Label(app, text="Password").pack()
password_entry = tk.Entry(app, show="*")
password_entry.pack(pady=5)

# User type switch (radio buttons)
user_type_var = tk.StringVar(value="student")
tk.Label(app, text="Login As").pack(pady=10)
student_rb = tk.Radiobutton(app, text="Student", variable=user_type_var, value="student")
parent_rb = tk.Radiobutton(app, text="Parent", variable=user_type_var, value="parent")
student_rb.pack()
parent_rb.pack()

# Child username field (only for parents)
child_frame = tk.Frame(app)
tk.Label(child_frame, text="Child Username").pack()
child_entry = tk.Entry(child_frame)
child_entry.pack(pady=5)

# Function to toggle child entry visibility
def on_user_type_change(*args):
    if user_type_var.get() == "parent":
        child_frame.pack(pady=5)
    else:
        child_frame.pack_forget()

user_type_var.trace_add('write', on_user_type_change)

# Initially hide child frame
on_user_type_change()

# Bind Enter key to login
app.bind('<Return>', login)

# Buttons
tk.Button(app, text="Login", command=login).pack(pady=10)
tk.Button(app, text="Sign Up", command=signup).pack(pady=5)

app.mainloop()
