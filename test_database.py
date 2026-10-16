
import sqlite3
import unittest
from unittest.mock import patch

import database


class TestKitchenInventory(unittest.TestCase):

    def test_add_item(self):
        # Use a temporary database for testing
        with patch.object(database, "DATABASE", ":memory:"):
            # For this test, use a temporary database file instead
            pass

        import tempfile
        import os

        with tempfile.TemporaryDirectory() as folder:
            test_db = os.path.join(folder, "test_inventory.db")

            with patch.object(database, "DATABASE", test_db):
                database.create_database()

                # Add a kitchen item
                database.add_inventory_item("Milk", 2)

                # Retrieve saved items
                items = database.get_inventory_items()

                # Check that the item was saved correctly
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0][1], "Milk")
                self.assertEqual(items[0][2], 2)


    def test_update_item(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as folder:
            test_db = os.path.join(folder, "test_inventory.db")

            with patch.object(database, "DATABASE", test_db):
                database.create_database()
                database.add_inventory_item("Milk", 2)

                items = database.get_inventory_items()
                item_id = items[0][0]

                database.update_inventory_item(item_id, "Milk", 5)

                updated_items = database.get_inventory_items()
                self.assertEqual(updated_items[0][2], 5)

    def test_delete_item(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as folder:
            test_db = os.path.join(folder, "test_inventory.db")

            with patch.object(database, "DATABASE", test_db):
                database.create_database()
                database.add_inventory_item("Eggs", 12)

                items = database.get_inventory_items()
                item_id = items[0][0]

                database.delete_inventory_item(item_id)

                remaining_items = database.get_inventory_items()
                self.assertEqual(len(remaining_items), 0)
    
    def test_low_stock_detection(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as folder:
            test_db = os.path.join(folder, "test_inventory.db")

            with patch.object(database, "DATABASE", test_db):
                database.create_database()

                database.add_inventory_item("Milk", 2, 3)
                database.add_inventory_item("Eggs", 12, 6)

                low_stock = database.get_low_stock_items()
                names = [item[1] for item in low_stock]

                self.assertIn("Milk", names)
                self.assertNotIn("Eggs", names)

    def test_shopping_list_no_duplicates(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as folder:
            test_db = os.path.join(folder, "test_inventory.db")

            with patch.object(database, "DATABASE", test_db):
                database.create_database()
                database.add_inventory_item("Bread", 0, 2)

                database.generate_shopping_list()
                database.generate_shopping_list()

                shopping_list = database.get_shopping_list()

                active_bread = [
                    task for task in shopping_list
                    if task[1] == "Bread" and task[2] == 0
                ]

                self.assertEqual(len(active_bread), 1)


if __name__ == "__main__":
    unittest.main()
