# login_screen.py (edited)
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
        writer.writerow(["username", "password", "balance", "rate", "user_type"])

def open_dashboard(username, user_type):
    app.destroy()
    subprocess.run(["python", "dashboard_screen.py", username, user_type])

def login(event=None):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == username and row[1] == password:
                open_dashboard(username, row[3])  # pass user_type
                return

    messagebox.showerror("Login Failed", "Invalid username or password.")

def signup():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    user_type = user_type_var.get()

    if not username or not password:
        messagebox.showwarning("Missing Info", "Both fields required.")
        return

    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == username:
                messagebox.showerror("Error", "Username already exists.")
                return

    with open(USER_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, "0", "0", user_type])

    messagebox.showinfo("Success", f"{user_type.capitalize()} account created! Logging you in...")
    open_dashboard(username, user_type)

# GUI Setup
app = tk.Tk()
app.title("ReWise Login")
app.geometry("375x667")

tk.Label(app, text="ReWise", font=("Helvetica", 24)).pack(pady=40)

tk.Label(app, text="Username").pack()
username_entry = tk.Entry(app)
username_entry.pack(pady=5)

tk.Label(app, text="Password").pack()
password_entry = tk.Entry(app, show="*")
password_entry.pack(pady=5)

# User type switch (radio buttons)
user_type_var = tk.StringVar(value="student")
tk.Label(app, text="Login As").pack(pady=10)
tk.Radiobutton(app, text="Student", variable=user_type_var, value="student").pack()
tk.Radiobutton(app, text="Parent", variable=user_type_var, value="parent").pack()

# Bind Enter key to login
app.bind('<Return>', login)

tk.Button(app, text="Login", command=login).pack(pady=10)
tk.Button(app, text="Sign Up", command=signup).pack(pady=5)

app.mainloop()
