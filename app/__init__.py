from flask import Flask, flash, redirect, request, render_template

from .config import config_by_name
from .extensions import db, migrate


def create_app(config_name="development"):
    app = Flask(__name__)

    # Завантаження конфігурації
    config_class = config_by_name.get(config_name, config_by_name["development"])
    app.config.from_object(config_class)

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)

    # Захист форм CSRF
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Обробка помилки завантаження завеликого файлу
    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash(
            "Файл завеликий. Максимальний розмір — 2 МБ.",
            "danger"
        )
        return redirect(request.path)

    # Реєстрація головного Blueprint
    from .views import main_bp
    app.register_blueprint(main_bp)

    # Реєстрація Blueprint користувачів
    from .users import users_bp
    app.register_blueprint(users_bp)

    # Реєстрація Blueprint товарів
    from .products import products_bp
    app.register_blueprint(products_bp)

    # Реєстрація Blueprint дописів
    from .posts import post_bp
    app.register_blueprint(post_bp)

    # Обробник помилки 404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app