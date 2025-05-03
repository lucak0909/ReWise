import tkinter as tk
from tkinter import messagebox
import subprocess
import csv
import os

USER_FILE = "users.csv"

# Ensure users.csv exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "balance"])  # Added "balance" column


def open_dashboard(username):
    app.destroy()
    subprocess.run(["python", "dashboard_screen.py", username])


def login(event=None):  # event is optional for Enter key
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == username and row[1] == password:
                open_dashboard(username)
                return

    messagebox.showerror("Login Failed", "Invalid username or password.")


def signup():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

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
        writer.writerow([username, password, "0"])  # New users start with $0

    messagebox.showinfo("Success", "Account created! Logging you in...")
    open_dashboard(username)


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

# Bind Enter key to login
app.bind('<Return>', login)

tk.Button(app, text="Login", command=login).pack(pady=10)
tk.Button(app, text="Sign Up", command=signup).pack(pady=5)

app.mainloop()
