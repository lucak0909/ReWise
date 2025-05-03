import tkinter as tk
from tkinter import messagebox
import csv
import sys
import os

USER_FILE = "users.csv"

# Get the username passed via command line
if len(sys.argv) < 2:
    raise Exception("Username required to load dashboard.")
username = sys.argv[1]

def load_balance():
    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    for row in rows:
        if row[0] == username:
            return int(row[2]) if len(row) > 2 else 0
    return 0

def update_balance_csv(new_balance):
    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows:
        if row[0] == username:
            if len(row) < 3:
                row.append(str(new_balance))
            else:
                row[2] = str(new_balance)

    with open(USER_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def fake_top_up():
    amount = entry.get()
    if amount.isdigit():
        current = int(balance_var.get())
        new_balance = current + int(amount)
        balance_var.set(str(new_balance))
        update_balance_csv(new_balance)
        messagebox.showinfo("Success", f"Fake topped up ${amount}")
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid", "Enter a numeric amount")

def open_upload():
    app.destroy()
    os.system("python upload_screen.py")

# GUI Setup
app = tk.Tk()
app.title("ReWise Dashboard")
app.geometry("375x667")

tk.Label(app, text=f"Welcome, {username}", font=("Helvetica", 16)).pack(pady=10)

tk.Label(app, text="Dashboard", font=("Helvetica", 20)).pack(pady=10)

balance_var = tk.StringVar(value=str(load_balance()))
tk.Label(app, text="Learning Balance:").pack()
tk.Label(app, textvariable=balance_var, font=("Helvetica", 16)).pack(pady=5)

tk.Label(app, text="Top Up Amount ($)").pack(pady=10)
entry = tk.Entry(app)
entry.pack()

tk.Button(app, text="Fake Top-Up", command=fake_top_up).pack(pady=10)
tk.Button(app, text="Go to Upload", command=open_upload).pack(pady=20)

app.mainloop()
