import tkinter as tk
from tkinter import filedialog, messagebox
from generate_quiz import extract_text, generate_mcq

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Choose a study file",
        filetypes=[("Text files", ["*.txt", "*.pdf", "*.pptx", "*.docx"])]
    )
    if file_path:
        try:
            text = extract_text(file_path)
            quiz = generate_mcq(text)
            quiz_output.delete("1.0", tk.END)
            quiz_output.insert(tk.END, quiz)
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate quiz:\n{e}")

# GUI Setup
app = tk.Tk()
app.title("ReWise - Upload")
app.geometry("375x667")

tk.Label(app, text="Upload Study Material", font=("Helvetica", 18)).pack(pady=20)

tk.Button(app, text="Select File", command=choose_file).pack(pady=10)

tk.Label(app, text="Generated Quiz:", font=("Helvetica", 14)).pack(pady=10)

quiz_output = tk.Text(app, height=20, wrap="word")
quiz_output.pack(padx=10, pady=10, fill="both", expand=True)

app.mainloop()
