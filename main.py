
import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    create_database,
    add_inventory_item,
    get_inventory_items,
    update_inventory_item,
    delete_inventory_item,
    get_low_stock_items
)

create_database()


def get_minimum(item_id):
    """Find the saved minimum quantity for an item."""
    import sqlite3
    from database import DATABASE

    with sqlite3.connect(DATABASE) as connection:
        result = connection.execute(
            "SELECT minimum_quantity FROM inventory WHERE id = ?",
            (item_id,)
        ).fetchone()

    return result[0] if result else 2


def read_fields():
    name = name_entry.get().strip()
    quantity = quantity_entry.get().strip()
    minimum = minimum_entry.get().strip()

    if not name or not quantity.isdecimal() or not minimum.isdecimal():
        messagebox.showerror(
            "Invalid Input",
            "Enter an item name and non-negative whole numbers."
        )
        return None

    return name, int(quantity), int(minimum)


def add_item():
    values = read_fields()
    if values is None:
        return

    add_inventory_item(*values)
    refresh_list()
    clear_fields()


def update_item():
    selected = inventory_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning", "Select an item first."
        )
        return

    values = read_fields()
    if values is None:
        return

    update_inventory_item(int(selected[0]), *values)
    refresh_list()
    clear_fields()


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


def refresh_list():
    for row in inventory_table.get_children():
        inventory_table.delete(row)

    for item_id, name, quantity in get_inventory_items():
        minimum = get_minimum(item_id)

        status = (
            "LOW STOCK"
            if quantity <= minimum
            else "IN STOCK"
        )

        inventory_table.insert(
            "", "end",
            iid=str(item_id),
            values=(name, quantity, minimum, status),
            tags=("low" if status == "LOW STOCK" else "good",)
        )


def show_low_stock():
    items = get_low_stock_items()

    if not items:
        messagebox.showinfo(
            "Low Stock",
            "All inventory items are above their minimum levels."
        )
        return

    details = "\n".join(
        f"{name}: {quantity} remaining (minimum {minimum})"
        for _, name, quantity, minimum in items
    )

    messagebox.showwarning(
        "Low-Stock Items",
        details
    )


def select_item(event):
    selected = inventory_table.selection()

    if selected:
        values = inventory_table.item(
            selected[0], "values"
        )

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[0])

        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[1])

        minimum_entry.delete(0, tk.END)
        minimum_entry.insert(0, values[2])


def clear_fields():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    minimum_entry.delete(0, tk.END)
    minimum_entry.insert(0, "2")


root = tk.Tk()
root.title("Kitchen Inventory Task Manager")
root.geometry("750x480")

ttk.Label(
    root,
    text="Kitchen Inventory Manager",
    font=("Arial", 18, "bold")
).pack(pady=15)

form = ttk.Frame(root)
form.pack(pady=10)

ttk.Label(form, text="Item Name:").grid(
    row=0, column=0, padx=5, pady=5
)
name_entry = ttk.Entry(form)
name_entry.grid(row=0, column=1, padx=5)

ttk.Label(form, text="Quantity:").grid(
    row=1, column=0, padx=5, pady=5
)
quantity_entry = ttk.Entry(form)
quantity_entry.grid(row=1, column=1, padx=5)

ttk.Label(form, text="Minimum Quantity:").grid(
    row=2, column=0, padx=5, pady=5
)
minimum_entry = ttk.Entry(form)
minimum_entry.grid(row=2, column=1, padx=5)
minimum_entry.insert(0, "2")

buttons = ttk.Frame(root)
buttons.pack(pady=10)

ttk.Button(
    buttons, text="Add Item", command=add_item
).pack(side="left", padx=5)

ttk.Button(
    buttons, text="Update Item", command=update_item
).pack(side="left", padx=5)

ttk.Button(
    buttons, text="Delete Item", command=delete_item
).pack(side="left", padx=5)

ttk.Button(
    root,
    text="Show Low-Stock Items",
    command=show_low_stock
).pack(pady=5)

inventory_table = ttk.Treeview(
    root,
    columns=("Name", "Quantity", "Minimum", "Status"),
    show="headings"
)

for column, heading in [
    ("Name", "Item Name"),
    ("Quantity", "Quantity"),
    ("Minimum", "Minimum"),
    ("Status", "Stock Status")
]:
    inventory_table.heading(column, text=heading)
    inventory_table.column(column, width=150)

inventory_table.tag_configure(
    "low", background="#ffcccc"
)
inventory_table.tag_configure(
    "good", background="#ddffdd"
)

inventory_table.pack(
    fill="both", expand=True, padx=20, pady=10
)

inventory_table.bind(
    "<<TreeviewSelect>>", select_item
)

refresh_list()
root.mainloop()
