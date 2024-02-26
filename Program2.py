import tkinter as tk
from tkinter import ttk, messagebox

class AddStudentDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Student")
        self.geometry("270x200")

        elements = [("Last Name:", tk.Entry), ("First Name:", tk.Entry), ("Middle Initial:", tk.Entry)]

        for i, (label_text, widget_type) in enumerate(elements):
            tk.Label(self, text=label_text, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            widget_type(self, font=("Arial", 10)).grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        tk.Button(self, text="Add Student", command=self.add_student, font=("Arial", 10), width=10).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

    def add_student(self):
        entries = [child for child in self.winfo_children() if isinstance(child, tk.Entry)]
        last_name, first_name, middle_initial = (entry.get() for entry in entries)

        if last_name and first_name:
            full_name = f"{last_name}, {first_name} {middle_initial}"
            app.add_student_from_dialog(full_name)
            self.destroy()
        else:
            messagebox.showerror("Error", "Please enter Last Name and First Name.")

class GradebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradebook")

        tk.Label(root, text="ELECTRONIC CLASS RECORD", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")
        self.students = []

        buttons = [
            ("Add Student", self.open_add_student_dialog),
            ("Add Grade", self.open_add_grade_dialog),
            ("Show Individual Grades", self.show_individual_grades),
            ("Show Class Averages", self.show_class_averages)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(root, text=text, command=command, font=("Arial", 11), width=100, height=2).grid(row=4 + i//2, column=i%2, pady=(10, 5), padx=(10, 5))

        columns = [("Name", "Student Name", 'center'), ("Average", "Average", 'center')]
        self.treeview_students = ttk.Treeview(root, columns=[col[0] for col in columns], show="headings", style="Treeview")

        for col, heading, align in columns:
            self.treeview_students.heading(col, text=heading, anchor=align)
            self.treeview_students.column(col, anchor=align)

        self.treeview_students.column("Name", width=150)
        self.treeview_students.column("Average", width=80)

        self.treeview_students.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.textbox_grades = tk.Text(root, font=("Arial", 10), height=5, width=30, state=tk.DISABLED)
        self.textbox_grades.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure((0, 1, 2), weight=1)

    def open_add_student_dialog(self):
        AddStudentDialog(self.root)

    def open_add_grade_dialog(self):
        AddGradeDialog(self.root, self.students, self.update_treeview)

    def add_student_from_dialog(self, full_name):
        self.students.append({"Name": full_name, "Grades": []})
        self.students.sort(key=lambda x: x["Name"].split(",")[0])
        self.update_treeview()
        self.textbox_grades.config(state=tk.NORMAL)

    def add_grade_from_dialog(self, student_index, grade_type, grade):
        quiz_number = sum(1 for g in self.students[student_index]["Grades"] if g["Type"].startswith("Quiz")) + 1
        new_grade_type = f"Quiz {quiz_number}"
        self.students[student_index]["Grades"].append({"Type": new_grade_type, "Grade": grade})
        self.update_treeview()

    def update_treeview(self, indices=None):
        self.treeview_students.delete(*self.treeview_students.get_children())
        students_to_display = self.students if indices is None else [self.students[i] for i in indices]
        for i, student in enumerate(students_to_display):
            average_grade = self.calculate_average_grade(student)
            capitalized_name = student["Name"].title()
            self.treeview_students.insert("", i, values=(capitalized_name, f"{average_grade:.2f}"))

    def calculate_average_grade(self, student):
        grades = student["Grades"]
        return sum(grade["Grade"] for grade in grades) / len(grades) if grades else 0.0

    def show_individual_grades(self):
        selected_indices = self.treeview_students.selection()
        if selected_indices:
            selected_item = selected_indices[0]
            student = next((self.students[i] for i, student_item in enumerate(self.treeview_students.get_children()) if
                            student_item == selected_item), None)

            if student:
                grades_text = "\n".join(f"{grade['Type']}: {grade['Grade']}" for grade in student["Grades"])
                self.textbox_grades.config(state=tk.NORMAL)
                self.textbox_grades.delete(1.0, tk.END)
                self.textbox_grades.insert(tk.END, grades_text)
                self.textbox_grades.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("No Selection", "Please select a student from the list.")
        else:
            messagebox.showinfo("No Selection", "Please select a student from the list.")

    def show_class_averages(self):
        if self.students:
            quiz_totals, quiz_counts = {}, {}
            for student in self.students:
                for grade in student["Grades"]:
                    if grade["Type"].startswith("Quiz"):
                        quiz_type = grade["Type"]
                        quiz_totals[quiz_type] = quiz_totals.get(quiz_type, 0) + grade["Grade"]
                        quiz_counts[quiz_type] = quiz_counts.get(quiz_type, 0) + 1

            class_averages = {quiz_type: total / count for quiz_type, total, count in
                              zip(quiz_totals.keys(), quiz_totals.values(), quiz_counts.values())}
            averages_text = "\n".join(f"{quiz_type}: {average:.2f}" for quiz_type, average in class_averages.items())
            self.textbox_grades.config(state=tk.NORMAL)
            self.textbox_grades.delete(1.0, tk.END)
            self.textbox_grades.insert(tk.END, averages_text)
            self.textbox_grades.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("No Students", "Please add students before calculating class averages.")

class AddGradeDialog(tk.Toplevel):
    def __init__(self, parent, students, update_treeview):
        super().__init__(parent)
        self.title("Add Grade")
        self.students = students
        self.update_treeview = update_treeview

        tk.Label(self, text="Select Student:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.listbox_students = tk.Listbox(self, font=("Arial", 10), selectmode=tk.SINGLE, exportselection=0)
        self.listbox_students.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        [self.listbox_students.insert(tk.END, student["Name"].title()) for student in students]

        tk.Label(self, text="Grade:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_grade = tk.Entry(self, font=("Arial", 10))
        self.entry_grade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.entry_grade.bind("<Return>", lambda event=None: self.add_grade())

        button = tk.Button(self, text="Add Grade", command=self.add_grade, font=("Arial", 10), width=30)
        button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        self.bind("<Return>", lambda event=None: self.add_grade())

    def add_grade(self):
        selected_index = self.listbox_students.curselection()
        if selected_index:
            student_name, grade = self.listbox_students.get(selected_index), self.entry_grade.get()
            if grade:
                student_index = next((i for i, student in enumerate(self.students) if student["Name"].title() == student_name),
                                     None)
                if student_index is not None:
                    app.add_grade_from_dialog(student_index, "General", float(grade))
                    self.destroy()
                else:
                    messagebox.showerror("Error", f"Student '{student_name}' not found.")
            else:
                messagebox.showerror("Error", "Please enter a grade.")
        else:
            messagebox.showerror("Error", "Please select a student.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    app = GradebookApp(root)
    root.mainloop()
