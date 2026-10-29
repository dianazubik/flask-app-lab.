from flask import Flask

app = Flask(__name__)


app.config.from_pyfile("../config.py")


from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
from flask import flash, redirect, request


@app.errorhandler(413)
def request_entity_too_large(error):
    flash(
        "Файл завеликий! Максимальний розмір запиту — 2 МБ.",
        "danger"
    )
    return redirect(request.path)

from . import views


from .users import users_bp
app.register_blueprint(users_bp)


from .products import products_bp
app.register_blueprint(products_bp)
