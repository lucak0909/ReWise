import tkinter as tk
from tkinter import messagebox
import csv
import sys
import os

USER_FILE = "users.csv"

if len(sys.argv) < 2:
    raise Exception("Username required to load dashboard.")
username = sys.argv[1]

def load_user_data():
    with open(USER_FILE, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows:
        if row[0] == username:
            # Pad with default values if missing
            while len(row) < 4:
                row.append("0")
            return rows, row
    raise Exception("User not found")

def update_user_data(new_balance, new_amount_per_question):
    for row in all_rows:
        if row[0] == username:
            row[2] = str(new_balance)
            row[3] = str(new_amount_per_question)

    with open(USER_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

def fake_top_up():
    amount = entry_topup.get()
    if amount.isdigit():
        current = int(balance_var.get())
        new_balance = current + int(amount)
        balance_var.set(str(new_balance))
        update_user_data(new_balance, amount_per_question_var.get())
        messagebox.showinfo("Success", f"Fake topped up ${amount}")
        entry_topup.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid", "Enter a numeric amount")

def save_amount_per_question():
    try:
        amt = float(amount_per_question_var.get())
        update_user_data(int(balance_var.get()), amt)
        messagebox.showinfo("Saved", f"Saved ${amt} per question")
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a valid number")

def open_upload():
    app.destroy()
    os.system("python upload_screen.py")

# Load user data
all_rows, current_user = load_user_data()
balance = int(current_user[2])
amount_per_question = float(current_user[3])

# GUI Setup
app = tk.Tk()
app.title("ReWise Dashboard")
app.geometry("375x667")

tk.Label(app, text=f"Welcome, {username}", font=("Helvetica", 16)).pack(pady=10)

tk.Label(app, text="Dashboard", font=("Helvetica", 20)).pack(pady=10)

balance_var = tk.StringVar(value=str(balance))
tk.Label(app, text="Learning Balance:").pack()
tk.Label(app, textvariable=balance_var, font=("Helvetica", 16)).pack(pady=5)

# Top-Up
tk.Label(app, text="Top Up Amount ($)").pack(pady=10)
entry_topup = tk.Entry(app)
entry_topup.pack()
tk.Button(app, text="Fake Top-Up", command=fake_top_up).pack(pady=10)

# Amount per question
amount_per_question_var = tk.StringVar(value=str(amount_per_question))
tk.Label(app, text="Amount Earned per Correct Question ($)").pack(pady=10)
tk.Entry(app, textvariable=amount_per_question_var).pack()
tk.Button(app, text="Save Rate", command=save_amount_per_question).pack(pady=5)

# Navigation
tk.Button(app, text="Go to Upload", command=open_upload).pack(pady=20)

app.mainloop()
