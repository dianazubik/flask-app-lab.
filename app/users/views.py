from flask import request, redirect, url_for, render_template, session, flash
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


