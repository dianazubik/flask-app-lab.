from flask import (request, redirect, url_for, render_template,session, flash, make_response)
from . import users_bp


@users_bp.route("/hi/<string:name>")  # /users/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("users/hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)


# Заглушка замість бази даних
VALID_USERNAME = "user1"
VALID_PASSWORD = "12345"


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Wrong data! Try again!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/profile.html", title="Профіль",
                           username=session["username"],
                           cookies=request.cookies)


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", type=int)  # None, якщо поле порожнє

    if not key or key == "session":
        flash("Вкажіть коректний ключ кукі (ключ «session» зарезервований).", "danger")
        return redirect(url_for("users.profile"))
    if max_age is not None and max_age <= 0:
        flash("Термін дії має бути більшим за 0 секунд.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age)
    flash(f"Кукі «{key}» успішно додано!", "success")
    return response


@users_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    if key == "session":
        flash("Кукі «session» видаляти не можна: це ваш вхід у систему.", "danger")
        return redirect(url_for("users.profile"))
    if key not in request.cookies:
        flash(f"Кукі з ключем «{key}» не знайдено.", "warning")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    flash(f"Кукі «{key}» успішно видалено!", "success")
    return response


@users_bp.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        if key != "session":  # щоб не розлогінити користувача
            response.delete_cookie(key)
    flash("Усі кукі успішно видалено!", "success")
    return response