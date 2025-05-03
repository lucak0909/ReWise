import tkinter as tk
from tkinter import messagebox
import csv
import sys
import random
import subprocess

USER_FILE     = "users.csv"
QUESTION_FILE = "questions.csv"

if len(sys.argv) < 2:
    raise Exception("Username required")
username = sys.argv[1]

def load_user_and_parent():
    """Load all users, find the student row and their parent row by matching child_username."""
    with open(USER_FILE, newline='') as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]

    # 1) Find the student record
    student = next((r for r in data if r[0] == username and r[4] == "student"), None)
    if not student:
        raise Exception("Student not found")

    # 2) Find the parent whose child_username == this student's username
    parent = next((r for r in data if r[5] == username and r[4] == "parent"), None)
    if not parent:
        raise Exception("Parent not found")

    # Parse numeric values
    stud_bal  = int(student[2])
    par_bal   = int(parent[2])
    rate      = float(parent[3])

    return rows, student, parent, stud_bal, par_bal, rate

def save_balances(all_rows, student_row, parent_row, new_stud_bal, new_par_bal):
    """Update both student and parent balances in-memory, then write out."""
    for row in all_rows[1:]:
        if row[0] == student_row[0]:
            row[2] = str(new_stud_bal)
        if row[0] == parent_row[0]:
            row[2] = str(new_par_bal)
    with open(USER_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

def load_questions():
    """Load MCQs from questions.csv into a list of dicts."""
    with open(QUESTION_FILE, newline='') as f:
        reader = csv.DictReader(f)
        qs = {}
        for r in reader:
            qid = r["question_id"]
            qs.setdefault(qid, {"text": r["question_text"], "answers": []})
            qs[qid]["answers"].append({
                "label":    r["answer_label"],
                "text":     r["answer_text"],
                "is_correct": r["is_correct"] == "TRUE"
            })
    return list(qs.values())

def select_answer(idx):
    global sel_idx
    sel_idx = idx
    for btn in ans_buttons:
        btn.config(relief=tk.RAISED)
    ans_buttons[idx].config(relief=tk.SUNKEN)

def submit_answer():
    global stud_bal, par_bal, q_idx
    if sel_idx is None:
        messagebox.showwarning("Choose One", "Please select an answer.")
        return

    ans = current_q["answers"][sel_idx]
    if not ans["is_correct"]:
        messagebox.showinfo("Sorry", "Incorrect.")
    else:
        # Enforce parent budget cap
        if par_bal < rate:
            messagebox.showinfo("Budget Exhausted",
                                "Your parent’s balance is too low to award more.")
            app.quit()
            return
        # Award
        stud_bal += rate
        par_bal  -= rate
        earnings_var.set(f"${stud_bal}")
        save_balances(all_rows, student_row, parent_row, stud_bal, par_bal)
        messagebox.showinfo("Well done", f"+${rate} credited!")

    next_question()

def next_question():
    global q_idx, current_q, sel_idx
    q_idx += 1
    sel_idx = None

    if q_idx >= len(questions):
        messagebox.showinfo("All Done", "You’ve completed the quiz!")
        app.quit()
        return

    current_q = questions[q_idx]
    question_lbl.config(text=current_q["text"])
    for i, a in enumerate(current_q["answers"]):
        ans_buttons[i].config(text=f"{a['label']}. {a['text']}", relief=tk.RAISED)

def logout():
    app.destroy()
    # re-open the login screen
    subprocess.run(["python", "login_screen.py"])

# — Initialization —
all_rows, student_row, parent_row, stud_bal, par_bal, rate = load_user_and_parent()
questions = load_questions()
random.shuffle(questions)

# — Build UI —
app = tk.Tk()
app.title("ReWise Quiz")
app.geometry("400x600")

# --- Log out button ---
logout_btn = tk.Button(app, text="Log Out", command=logout)
# pack it in the top-right corner
logout_btn.pack(anchor="ne", padx=10, pady=5)

tk.Label(app, text=f"Hello, {username}", font=("Helvetica", 16)).pack(pady=10)
tk.Label(app, text="Your Earnings:", font=("Helvetica", 14)).pack()
earnings_var = tk.StringVar(value=f"${stud_bal}")
tk.Label(app, textvariable=earnings_var, font=("Helvetica", 20)).pack(pady=5)

question_lbl = tk.Label(app, text="", wraplength=360, font=("Helvetica", 14))
question_lbl.pack(pady=20)

ans_buttons = []
sel_idx = None
for i in range(4):
    b = tk.Button(app, text="", width=40, command=lambda i=i: select_answer(i))
    b.pack(pady=4)
    ans_buttons.append(b)

tk.Button(app, text="Submit", command=submit_answer).pack(pady=20)

q_idx = -1
current_q = None
next_question()

app.mainloop()
