import tkinter as tk
from tkinter import messagebox, simpledialog

class InventoryApp:
    def __init__(self):
        self.inventory = {
            'Motherboard': 0,
            'Hard Disk': 0,
            'Diskette': 0,
            'Compact Disk': 0,
            'Memory Card': 0
        }

        self.root = tk.Tk()
        self.root.title("Inventory Management")

        self.root.geometry("400x300")

        self.root.configure(bg="#004b8d")

        self.label = tk.Label(self.root, text="Computer Hardware Inventory", bg="#e6e6e6")
        self.label.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Items", command=self.add_items)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self.root, text="Remove Items", command=self.remove_items)
        self.remove_button.pack(pady=5)

        self.display_button = tk.Button(self.root, text="Display Inventory", command=self.display_inventory)
        self.display_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.pack(pady=10)

    def add_items(self):
        inventory_str = "Select an item to add:\n"
        for i, (product, quantity) in enumerate(self.inventory.items(), start=1):
            inventory_str += f"{i}. {product}\n"

        selected_index = simpledialog.askinteger("Add Items", inventory_str)
        if selected_index is not None and 1 <= selected_index <= len(self.inventory):
            product = list(self.inventory.keys())[selected_index - 1]
            quantity = simpledialog.askinteger("Add Items", f"Enter quantity for {product}:")
            if quantity:
                self.inventory[product] = self.inventory.get(product, 0) + quantity
                messagebox.showinfo("Success", f"{quantity} {product}(s) added to inventory.")

    def remove_items(self):
        inventory_str = "Select an item to remove:\n"
        for i, (product, quantity) in enumerate(self.inventory.items(), start=1):
            inventory_str += f"{i}. {product}\n"

        selected_index = simpledialog.askinteger("Remove Items", inventory_str)
        if selected_index is not None and 1 <= selected_index <= len(self.inventory):
            product = list(self.inventory.keys())[selected_index - 1]
            if product in self.inventory and self.inventory[product] > 0:
                quantity = simpledialog.askinteger("Remove Items", f"Enter quantity for {product}:")
                if quantity:
                    if quantity <= self.inventory[product]:
                        self.inventory[product] -= quantity
                        messagebox.showinfo("Success", f"{quantity} {product}(s) removed from inventory.")
                    else:
                        messagebox.showerror("Error", "Not enough quantity in inventory.")
            else:
                messagebox.showerror("Error", "Product not found in inventory or quantity is already zero.")

    def display_inventory(self):
        inventory_str = "Current Inventory:\n"
        for product, quantity in self.inventory.items():
            inventory_str += f"{product}: {quantity}\n"
        messagebox.showinfo("Inventory", inventory_str)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InventoryApp()
    app.run()
