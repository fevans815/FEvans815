
import sqlite3

DATABASE = "kitchen_inventory.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0)
        )
    """)

    connection.commit()
    connection.close()


def add_inventory_item(name, quantity):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO inventory (name, quantity) VALUES (?, ?)",
        (name, quantity)
    )

    connection.commit()
    connection.close()


def get_inventory_items():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, quantity FROM inventory")
    items = cursor.fetchall()

    connection.close()
    return items


def update_inventory_item(item_id, name, quantity):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE inventory SET name = ?, quantity = ? WHERE id = ?",
        (name, quantity, item_id)
    )

    connection.commit()
    connection.close()


def delete_inventory_item(item_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM inventory WHERE id = ?",
        (item_id,)
    )

    connection.commit()
    connection.close()
