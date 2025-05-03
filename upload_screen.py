import tkinter as tk
from tkinter import filedialog, messagebox
from generate_quiz import generate_mcq_from_file
from parser import parse_raw_output
import subprocess


raw_output = ""  # Global or module-level to reuse after generation

def select_file():
    global raw_output
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            output = generate_mcq_from_file(file_path)
            raw_output = output  # Save for parser use
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error", f"Quiz generation failed:\n{e}")

def parse_output():
    global raw_output
    if not raw_output.strip():
        messagebox.showwarning("No Data", "No quiz output to parse.")
        return
    try:
        parse_raw_output(raw_output)
        messagebox.showinfo("Success", "Quiz saved to questions.csv.")
    except Exception as e:
        messagebox.showerror("Parse Error", str(e))

def logout():
    app.destroy()
    # re-open the login screen
    subprocess.run(["python", "login_screen.py"])

# UI Setup
app = tk.Tk()
app.title("Upload and Generate Quiz")
app.geometry("500x600")

# --- Log out button ---
logout_btn = tk.Button(app, text="Log Out", command=logout)
# pack it in the top-right corner
logout_btn.pack(anchor="ne", padx=10, pady=5)


tk.Button(app, text="Select File", command=select_file).pack(pady=10)

text_output = tk.Text(app, wrap=tk.WORD)
text_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

tk.Button(app, text="Parse Output", command=parse_output).pack(pady=10)

app.mainloop()
