
import unittest

from app import app
from app.products import storage


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_page(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Keyboard", response.data)

    def test_product_detail_page(self):
        products = storage.get_all_products()

        if not products:
            self.skipTest("У базі немає товарів для перевірки")

        product_id = products[0]["id"]
        response = self.client.get(f"/products/{product_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            products[0]["name"].encode("utf-8"),
            response.data
        )

    def test_product_not_found(self):
        response = self.client.get("/products/999999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
