
from datetime import datetime
from pathlib import Path
from decimal import Decimal
from uuid import uuid4

from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    request,
    current_app
)
from werkzeug.utils import secure_filename

from . import products_bp
from .forms import ProductForm
from .storage import (
    get_all_products,
    get_product,
    add_product,
    update_product,
    delete_product
)


UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"


def save_image(file):
    """Безпечно зберігає зображення та повертає відносний шлях."""
    if not file or not file.filename:
        return None

    original_name = secure_filename(file.filename)
    extension = Path(original_name).suffix.lower()

    if extension not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("Недозволений формат зображення")

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{extension}"
    file.save(UPLOAD_FOLDER / filename)

    return f"uploads/{filename}"


@products_bp.route("/product")
def product_list():
    products = get_all_products()

    return render_template(
        "products/products.html",
        title="Товари",
        products=products
    )


@products_bp.route("/products/")
def legacy_product_list():
    return render_template(
        "products/products.html",
        title="Товари",
        products=get_all_products()
    )


@products_bp.route("/product/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = save_image(form.image.data)

            product_data = {
                "name": form.name.data.strip(),
                "content": form.content.data,
                "price": str(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path,
                "created_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

            add_product(product_data)

            flash("Товар успішно додано!", "success")
            return redirect(url_for("products.product_list"))

        except Exception:
            current_app.logger.exception(
                "Помилка під час додавання товару"
            )
            flash("Не вдалося додати товар.", "danger")

    return render_template(
        "products/product_form.html",
        title="Додавання товару",
        form=form
    )


@products_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product
    )

@products_bp.route("/products/<int:product_id>")
def legacy_product_detail(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product
    ) 


@products_bp.route(
    "/product/<int:product_id>/edit",
    methods=["GET", "POST"]
)
def product_edit(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    form = ProductForm()

    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(str(product["price"]))
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    if form.validate_on_submit():
        try:
            image_path = product.get("image")

            if form.image.data and form.image.data.filename:
                new_image = save_image(form.image.data)
                if new_image:
                    image_path = new_image

            product_data = {
                "name": form.name.data.strip(),
                "content": form.content.data,
                "price": str(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path
            }

            update_product(product_id, product_data)

            flash("Товар успішно оновлено!", "success")
            return redirect(
                url_for(
                    "products.product_detail",
                    product_id=product_id
                )
            )

        except Exception:
            current_app.logger.exception(
                "Помилка під час редагування товару"
            )
            flash("Не вдалося оновити товар.", "danger")

    return render_template(
        "products/product_form.html",
        title="Редагування товару",
        form=form,
        product=product
    )


@products_bp.route(
    "/product/<int:product_id>/delete",
    methods=["POST"]
)
def product_delete(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    delete_product(product_id)

    flash("Товар видалено.", "success")
    return redirect(url_for("products.product_list"))
 