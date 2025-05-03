import tkinter as tk
from tkinter import messagebox
import csv
import sys
import os
import subprocess


USER_FILE = "users.csv"

if len(sys.argv) < 3:
    raise Exception("Username and user_type required")
username, user_type = sys.argv[1], sys.argv[2]

def load_user_data():
    with open(USER_FILE, "r", newline='') as f:
        reader = list(csv.reader(f))
    header, rows = reader[0], reader[1:]
    for row in rows:
        if row[0] == username:
            # ensure full length
            while len(row) < len(header):
                row.append("")
            return reader, row
    raise Exception("User not found")

def update_user_data(new_balance, new_rate):
    # update both parent and their child
    child_username = current_user[5]  # assuming 6th column is child_username
    for row in all_rows[1:]:
        if row[0] == username:
            row[2] = str(new_balance)      # balance
            row[3] = str(new_rate)         # rate
        if user_type == "parent" and row[0] == child_username:
            row[3] = str(new_rate)         # propagate rate to child
    # write back
    with open(USER_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

def fake_top_up():
    amt = entry_topup.get().strip()
    if amt.isdigit():
        new_bal = balance + int(amt)
        balance_var.set(str(new_bal))
        update_user_data(new_bal, amount_per_question)
        messagebox.showinfo("Success", f"Fake topped up ${amt}")
        entry_topup.delete(0, tk.END)
    else:
        messagebox.showwarning("Invalid", "Enter a numeric amount")

def save_amount_per_question():
    global amount_per_question
    try:
        amt = float(amount_per_question_var.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a valid number")
        return

    amount_per_question = amt
    update_user_data(balance, amount_per_question)
    messagebox.showinfo("Saved", f"Saved ${amt} per question\n(also updated your child’s rate)")

def open_upload():
    app.destroy()
    os.system("python upload_screen.py")

def logout():
    app.destroy()
    # re-open the login screen
    subprocess.run(["python", "login_screen.py"])

# Load user data
all_rows, current_user = load_user_data()
header = all_rows[0]
balance = int(current_user[2])
amount_per_question = float(current_user[3])

# GUI Setup
app = tk.Tk()
app.title("ReWise Dashboard (Parent)" if user_type=="parent" else "ReWise Dashboard")
app.geometry("375x667")

# --- Log out button ---
logout_btn = tk.Button(app, text="Log Out", command=logout)
# pack it in the top-right corner
logout_btn.pack(anchor="ne", padx=10, pady=5)


tk.Label(app, text=f"Welcome, {username}", font=("Helvetica", 16)).pack(pady=10)
tk.Label(app, text="Dashboard", font=("Helvetica", 20)).pack(pady=10)

# Balance display
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
if user_type == "parent":
    tk.Button(app, text="Go to Upload", command=open_upload).pack(pady=20)

app.mainloop()
