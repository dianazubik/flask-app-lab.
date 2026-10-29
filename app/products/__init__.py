
from flask import Blueprint

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
    static_url_path="/products/static"
)

from . import views
