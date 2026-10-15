
import sqlite3

DATABASE = "kitchen_inventory.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            minimum_quantity INTEGER NOT NULL DEFAULT 2
                CHECK(minimum_quantity >= 0)
        )
    """)

    # Upgrade an existing Milestone 1 database.
    cursor.execute("PRAGMA table_info(inventory)")
    columns = [column[1] for column in cursor.fetchall()]

    if "minimum_quantity" not in columns:
        cursor.execute("""
            ALTER TABLE inventory
            ADD COLUMN minimum_quantity INTEGER NOT NULL DEFAULT 2
        """)

    connection.commit()
    connection.close()


def add_inventory_item(name, quantity, minimum_quantity=2):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO inventory (name, quantity, minimum_quantity)
        VALUES (?, ?, ?)
    """, (name, quantity, minimum_quantity))

    connection.commit()
    connection.close()


def get_inventory_items():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, quantity
        FROM inventory
    """)

    items = cursor.fetchall()
    connection.close()
    return items


def update_inventory_item(item_id, name, quantity,
                          minimum_quantity=None):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if minimum_quantity is None:
        cursor.execute("""
            UPDATE inventory
            SET name = ?, quantity = ?
            WHERE id = ?
        """, (name, quantity, item_id))
    else:
        cursor.execute("""
            UPDATE inventory
            SET name = ?, quantity = ?, minimum_quantity = ?
            WHERE id = ?
        """, (name, quantity, minimum_quantity, item_id))

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


def get_low_stock_items():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, quantity, minimum_quantity
        FROM inventory
        WHERE quantity <= minimum_quantity
        ORDER BY name
    """)

    items = cursor.fetchall()
    connection.close()
    return items
