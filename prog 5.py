import tkinter as tk
from tkinter import messagebox, simpledialog

class AddressBookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Address Book")

        self.people = []
        self.phonenumbers = []

        # Load existing data
        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack()

        # Dropdown Menu for Function Selection
        self.function_var = tk.StringVar()
        self.function_var.set("Select Function")

        self.function_menu = tk.OptionMenu(main_frame, self.function_var,
                                           "Select Function", "Search", "Add", "Edit", "Delete")
        self.function_menu.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Labels and Entry Widgets
        self.name_label = tk.Label(main_frame, text="Enter person's name:")
        self.name_label.grid(row=1, column=0, pady=5, sticky="w")
        self.name_entry = tk.Entry(main_frame)
        self.name_entry.grid(row=1, column=1, pady=5, sticky="ew")

        self.phone_label = tk.Label(main_frame, text="Enter phone number:")
        self.phone_label.grid(row=2, column=0, pady=5, sticky="w")
        self.phone_entry = tk.Entry(main_frame)
        self.phone_entry.grid(row=2, column=1, pady=5, sticky="ew")

        # Buttons
        self.perform_button = tk.Button(main_frame, text="Perform", command=self.perform_function)
        self.perform_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Save Button
        self.save_button = tk.Button(main_frame, text="Save Data", command=self.save_data)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def perform_function(self):
        selected_function = self.function_var.get()

        if selected_function == "Search":
            self.show_phone_entry()
            self.search()
        elif selected_function in ["Add", "Edit", "Delete"]:
            self.show_phone_entry()
            if selected_function == "Add":
                self.add_entry()
            elif selected_function == "Edit":
                self.edit_entry()
            elif selected_function == "Delete":
                self.delete_entry()
        else:
            messagebox.showwarning("Error", "Please select a valid function.")

    def show_phone_entry(self):
        self.phone_label.grid(row=2, column=0, pady=5, sticky="w")
        self.phone_entry.grid(row=2, column=1, pady=5, sticky="ew")

    def search(self):
        name = self.name_entry.get().lower()
        if name in [person.lower() for person in self.people]:
            index = self.people.index(next(person for person in self.people if person.lower() == name))
            result_message = f"{name}'s phone number is {self.phonenumbers[index]}"
            messagebox.showinfo("Result", result_message)
        else:
            messagebox.showinfo("Result", "No matching name was found.")
        self.clear_entries()

    def add_entry(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if name and phone:
            self.people.append(name)
            self.phonenumbers.append(phone)
            messagebox.showinfo("Success", "Entry added successfully.")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Please enter both name and phone number.")

    def edit_entry(self):
        name = self.name_entry.get().lower()
        if name in [person.lower() for person in self.people]:
            index = self.people.index(next(person for person in self.people if person.lower() == name))
            new_phone = simpledialog.askstring("Edit Entry", f"Enter new phone number for {name}:")
            if new_phone:
                self.phonenumbers[index] = new_phone
                messagebox.showinfo("Success", f"{name}'s phone number updated.")
                self.clear_entries()
            else:
                messagebox.showwarning("Error", "Please enter a new phone number.")
        else:
            messagebox.showwarning("Error", "No matching name was found for editing.")

    def delete_entry(self):
        name = self.name_entry.get().lower()
        if name in [person.lower() for person in self.people]:
            index = self.people.index(next(person for person in self.people if person.lower() == name))
            confirmation = messagebox.askyesno("Delete Entry", f"Do you want to delete {name}'s entry?")
            if confirmation:
                del self.people[index]
                del self.phonenumbers[index]
                messagebox.showinfo("Success", f"{name}'s entry deleted.")
                self.clear_entries()
        else:
            messagebox.showwarning("Error", "No matching name was found for deletion.")

    def save_data(self):
        with open("address_book_data.txt", "w") as file:
            for person, phone in zip(self.people, self.phonenumbers):
                file.write(f"{person},{phone}\n")
        messagebox.showinfo("Save", "Data saved successfully.")

    def load_data(self):
        try:
            with open("address_book_data.txt", "r") as file:
                for line in file:
                    person, phone = line.strip().split(',')
                    self.people.append(person)
                    self.phonenumbers.append(phone)
        except FileNotFoundError:
            open("address_book_data.txt", "w").close()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AddressBookApp(root)
    root.mainloop()
