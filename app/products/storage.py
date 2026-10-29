
import atexit
from pathlib import Path
from tinydb import TinyDB


# Коренева папка проєкту
BASE_DIR = Path(__file__).resolve().parents[2]

# Шлях до JSON-файлу
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "products.json"

# Підключення до бази даних
db = TinyDB(str(DB_PATH), encoding="utf-8")
products_table = db.table("products")
atexit.register(db.close)

def get_all_products():
    """Повертає всі товари."""
    return products_table.all()


def get_product(product_id):
    """Знаходить товар за його id."""
    return products_table.get(
        lambda product: product.get("id") == product_id
    )


def add_product(product_data):
    """Додає товар з унікальним числовим id."""
    existing_ids = [
        product.get("id", 0)
        for product in products_table.all()
    ]

    new_id = max(existing_ids, default=0) + 1
    product_data["id"] = new_id

    products_table.insert(product_data)
    return new_id


def update_product(product_id, product_data):
    """Оновлює товар, не змінюючи його id."""
    product_data.pop("id", None)
    product_data.pop("created_at", None)

    products_table.update(
        product_data,
        lambda product: product.get("id") == product_id
    )


def delete_product(product_id):
    """Видаляє товар за id."""
    products_table.remove(
        lambda product: product.get("id") == product_id
    )
