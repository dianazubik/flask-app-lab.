import unittest
from app import app


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_page(self):
        """Тест списку товарів /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_product_detail_page(self):
        """Тест детальної сторінки товару /products/1."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        """Тест неіснуючого товару /products/99."""
        response = self.client.get("/products/99")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()