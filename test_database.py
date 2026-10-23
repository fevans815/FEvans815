
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



    def test_exact_minimum_is_low_stock(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                database.add_inventory_item("Rice", 3, 3)
                names = [item[1] for item in database.get_low_stock_items()]
                self.assertIn("Rice", names)

    def test_above_minimum_is_not_low_stock(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                database.add_inventory_item("Rice", 4, 3)
                names = [item[1] for item in database.get_low_stock_items()]
                self.assertNotIn("Rice", names)

    def test_multiple_low_stock_items_generate_shopping_tasks(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                database.add_inventory_item("Milk", 1, 3)
                database.add_inventory_item("Bread", 0, 2)
                database.add_inventory_item("Eggs", 12, 6)
                database.generate_shopping_list()
                names = [task[1] for task in database.get_shopping_list()]
                self.assertCountEqual(names, ["Milk", "Bread"])

    def test_mark_shopping_task_purchased(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                database.add_inventory_item("Milk", 0, 2)
                database.generate_shopping_list()
                task_id = database.get_shopping_list()[0][0]
                database.mark_task_purchased(task_id)
                tasks = database.get_shopping_list()
                self.assertEqual(tasks[0][2], 1)

    def test_negative_quantity_rejected_by_database(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                with self.assertRaises(sqlite3.IntegrityError):
                    database.add_inventory_item("Milk", -1, 2)
                self.assertEqual(database.get_inventory_items(), [])


    def test_minimum_quantity_update_changes_low_stock_status(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                database.add_inventory_item("Pasta", 5, 2)
                item_id = database.get_inventory_items()[0][0]
                self.assertNotIn("Pasta", [item[1] for item in database.get_low_stock_items()])
                database.update_inventory_item(item_id, "Pasta", 5, 6)
                self.assertIn("Pasta", [item[1] for item in database.get_low_stock_items()])

    def test_purchased_shopping_task_persists_after_reopening(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(database, "DATABASE", os.path.join(folder, "test.db")):
                database.create_database()
                database.add_inventory_item("Flour", 0, 2)
                database.generate_shopping_list()
                task_id = database.get_shopping_list()[0][0]
                database.mark_task_purchased(task_id)
                database.generate_shopping_list()
                tasks = database.get_shopping_list()
                self.assertEqual(len(tasks), 1)
                self.assertEqual(tasks[0], (task_id, "Flour", 1))

if __name__ == "__main__":
    unittest.main()
