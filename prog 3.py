import tkinter as tk
from tkinter import messagebox

def encrypt(text):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if (char.isupper()):
            result += chr((ord(char) + 1 - 65) % 26 + 65)
        else:
            result += chr((ord(char) + 1 - 97) % 26 + 97)
    return result

def on_click():
    try:
        text = text_entry.get()
        if text.isalpha():
            result = encrypt(text)
            result_label.config(text="The encrypted text is: " + result)
            messagebox.showinfo("Encryption Successful", "Your text has been successfully encrypted!")
            try_again_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        else:
            messagebox.showerror("Error", "Invalid input. Please enter a text string.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a text string.")

def try_again():
    text_entry.delete(0, tk.END)
    result_label.config(text="")
    try_again_button.grid_forget()

app = tk.Tk()
app.title("Encryptor")
app.configure(bg="#2c3e50")

frame = tk.Frame(app, bg="#2c3e50")
frame.pack(padx=50, pady=50)

text_label = tk.Label(frame, text="Enter text:", bg="#2c3e50", fg="white")
text_label.grid(row=0, column=0, padx=5, pady=5)

text_entry = tk.Entry(frame)
text_entry.grid(row=0, column=1, padx=5, pady=5)

encrypt_button = tk.Button(frame, text="Encrypt", command=on_click, bg="#2980b9", fg="white")
encrypt_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

result_label = tk.Label(frame, text="", bg="#2c3e50", fg="white")
result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

try_again_button = tk.Button(frame, text="Try Again", command=try_again, bg="#2980b9", fg="white")

app.mainloop()