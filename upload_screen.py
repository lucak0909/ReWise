import tkinter as tk
from tkinter import filedialog, messagebox

def choose_file():
    file_path = filedialog.askopenfilename(title="Choose a study file")
    if file_path:
        messagebox.showinfo("File Selected", f"You chose:\n{file_path}")

app = tk.Tk()
app.title("ReWise - Upload")
app.geometry("375x667")

tk.Label(app, text="Upload Study Material", font=("Helvetica", 18)).pack(pady=30)

tk.Button(app, text="Select File", command=choose_file).pack(pady=20)

app.mainloop()
