
import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    create_database,
    add_inventory_item,
    get_inventory_items,
    update_inventory_item,
    delete_inventory_item
)

# Create the database and load saved inventory
create_database()
inventory = get_inventory_items()

def add_item():
    name = name_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if not name or not quantity.isdecimal():
        messagebox.showerror("Error", "Enter a valid name and quantity.")
        return

    add_inventory_item(name, int(quantity))
    refresh_list()
    clear_fields()


def update_item():
    selected = inventory_table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an item first.")
        return

    name = name_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if not name or not quantity.isdecimal():
        messagebox.showerror("Error", "Enter a valid name and quantity.")
        return

    update_inventory_item(int(selected[0]), name, int(quantity))
    refresh_list()
    clear_fields()

def refresh_list():
    for row in inventory_table.get_children():
        inventory_table.delete(row)

    for item_id, name, quantity in get_inventory_items():
        inventory_table.insert(
            "", "end",
            iid=str(item_id),
            values=(name, quantity)
        )


def select_item(event):
    selected = inventory_table.selection()

    if selected:
        values = inventory_table.item(selected[0], "values")

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[0])

        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[1])


def delete_item():
    selected = inventory_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning", "Select an item first."
        )
        return

    delete_inventory_item(int(selected[0]))
    refresh_list()
    clear_fields()


def clear_fields():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Kitchen Inventory Task Manager")
root.geometry("550x420")

ttk.Label(root, text="Kitchen Inventory Manager",
          font=("Arial", 18, "bold")).pack(pady=15)

form = ttk.Frame(root)
form.pack(pady=10)

ttk.Label(form, text="Item Name:").grid(row=0, column=0, padx=5)
name_entry = ttk.Entry(form)
name_entry.grid(row=0, column=1, padx=5)

ttk.Label(form, text="Quantity:").grid(row=1, column=0, padx=5, pady=10)
quantity_entry = ttk.Entry(form)
quantity_entry.grid(row=1, column=1, padx=5)

buttons = ttk.Frame(root)
buttons.pack(pady=10)

ttk.Button(buttons, text="Add Item", command=add_item).pack(
    side="left", padx=5)
ttk.Button(buttons, text="Update Item", command=update_item).pack(
    side="left", padx=5)
ttk.Button(buttons, text="Delete Item", command=delete_item).pack(
    side="left", padx=5)

inventory_table = ttk.Treeview(
    root, columns=("Name", "Quantity"), show="headings"
)
inventory_table.heading("Name", text="Item Name")
inventory_table.heading("Quantity", text="Quantity")
inventory_table.pack(fill="both", expand=True, padx=20, pady=10)
inventory_table.bind("<<TreeviewSelect>>", select_item)

refresh_list()
root.mainloop()