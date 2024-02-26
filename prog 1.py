import random
import tkinter as tk
from tkinter import messagebox

class MultiplicationGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Multiplication Game")

        self.master.configure(bg='#004b8d')

        self.points = 0
        self.deduction = 5
        self.generate_question()

        self.label_question = tk.Label(master, text=f"How much is {self.num1} times {self.num2}?", font=('Arial', 14), bg='#E1F5FE')
        self.label_question.pack(pady=10)

        self.entry = tk.Entry(master, font=('Arial', 12))
        self.entry.pack(pady=10)

        self.check_button = tk.Button(master, text="Check Answer", command=self.check_answer, bg='white', fg='black', font=('Arial', 12))
        self.check_button.pack(pady=10)

        self.label_score = tk.Label(master, text=f"Score: {self.points}", font=('Arial', 12), bg='#E1F5FE')
        self.label_score.pack(pady=10)

    def generate_question(self):
        self.num1 = random.randint(1, 9)
        self.num2 = random.randint(1, 9)
        self.correct_answer = self.num1 * self.num2

    def check_answer(self):
        user_answer = self.entry.get()

        try:
            user_answer = int(user_answer)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        if user_answer == self.correct_answer:
            messagebox.showinfo("Correct", "You are correct!")
            self.points += 5
            self.label_score.config(text=f"Score: {self.points}")
            self.generate_question()
            self.label_question.config(text=f"How much is {self.num1} times {self.num2}?")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror("Incorrect", "Incorrect. Deducting 5 points.")
            self.points -= self.deduction
            self.label_score.config(text=f"Score: {self.points}")

            if self.points <= 0:
                messagebox.showinfo("Game Over", "Game Over! You've run out of points.")
                self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    root.resizable(False, False)  # Disable resizing
    game = MultiplicationGame(root)
    root.mainloop()
