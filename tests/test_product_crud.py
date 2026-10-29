
import tempfile
import unittest
import os

from tinydb import TinyDB
from app import app
from app.products import storage


class ProductCRUDTestCase(unittest.TestCase):

    def setUp(self):
        # Створюємо тимчасову базу даних для тесту
        temp = tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False
        )
        temp.close()

        self.temp_path = temp.name
        self.db = TinyDB(self.temp_path)

        # Підміняємо таблицю товарів тестовою
        self.original_table = storage.products_table
        storage.products_table = self.db.table("products")

        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def tearDown(self):
        # Повертаємо справжню таблицю
        storage.products_table = self.original_table

        self.db.close()
        os.unlink(self.temp_path)

    def create_product(self):
        return self.client.post(
            "/product/add",
            data={
                "name": "Test Mouse",
                "content": "Тестовий опис",
                "price": "25.50",
                "category": "accessories",
                "quantity": "10",
            },
            follow_redirects=True
        )

    def test_create_product(self):
        response = self.create_product()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(storage.get_all_products()), 1)
        self.assertEqual(
            storage.get_all_products()[0]["name"],
            "Test Mouse"
        )

    def test_read_product(self):
        self.create_product()
        product = storage.get_all_products()[0]

        response = self.client.get(
            f"/product/{product['id']}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Mouse", response.data)

    def test_update_product(self):
        self.create_product()
        product = storage.get_all_products()[0]

        old_id = product["id"]
        old_date = product["created_at"]

        response = self.client.post(
            f"/product/{old_id}/edit",
            data={
                "name": "Updated Mouse",
                "content": "Оновлений опис",
                "price": "30.00",
                "category": "accessories",
                "quantity": "15",
            },
            follow_redirects=True
        )

        updated = storage.get_product(old_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated["name"], "Updated Mouse")
        self.assertEqual(updated["id"], old_id)
        self.assertEqual(updated["created_at"], old_date)

    def test_delete_product(self):
        self.create_product()
        product = storage.get_all_products()[0]

        response = self.client.post(
            f"/product/{product['id']}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(storage.get_all_products()), 0)

    def test_product_not_found(self):
        response = self.client.get("/product/999999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
