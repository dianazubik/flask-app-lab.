
from datetime import datetime

from flask import render_template, redirect, url_for, flash, abort, request

from . import post_bp
from .models import Post, Tag
from .forms import PostForm
from app.extensions import db
from app.users.models import User


# Створення нового допису
@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    # Отримуємо авторів із бази даних
    authors = db.session.scalars(
        db.select(User).order_by(User.id)
    ).all()

    form.author_id.choices = [
        (author.id, author.username) for author in authors
    ]

    # Отримуємо теги з бази даних
    tags = db.session.scalars(
        db.select(Tag).order_by(Tag.id)
    ).all()

    form.tags.choices = [
        (tag.id, tag.name) for tag in tags
    ]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data or datetime.utcnow(),
            user_id=form.author_id.data
        )

        # Додаємо вибрані теги до допису
        post.tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()

        db.session.add(post)
        db.session.commit()

        flash("Допис успішно створено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/add_post.html",
        title="Створення допису",
        form=form
    )


# Перегляд усіх активних дописів
@post_bp.route("/", methods=["GET"])
def all_posts():
    posts = db.session.execute(
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    ).scalars().all()

    return render_template(
        "posts/all_posts.html",
        title="Усі дописи",
        posts=posts
    )


# Перегляд одного допису
@post_bp.route("/<int:post_id>", methods=["GET"])
def detail_post(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    return render_template(
        "posts/detail_post.html",
        title=post.title,
        post=post
    )


# Редагування допису
@post_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    form = PostForm()

    # Отримуємо авторів із бази даних
    authors = db.session.scalars(
        db.select(User).order_by(User.id)
    ).all()

    form.author_id.choices = [
        (author.id, author.username) for author in authors
    ]

    # Отримуємо теги з бази даних
    tags = db.session.scalars(
        db.select(Tag).order_by(Tag.id)
    ).all()

    form.tags.choices = [
        (tag.id, tag.name) for tag in tags
    ]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data or post.posted
        post.user_id = form.author_id.data

        # Оновлюємо теги допису
        post.tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()

        db.session.commit()

        flash("Допис успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]

    return render_template(
        "posts/add_post.html",
        title="Редагування допису",
        form=form,
        post=post
    )


# Підтвердження та видалення допису
@post_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.session.get(Post, post_id)

    if post is None:
        abort(404)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        flash("Допис успішно видалено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/delete_confirm.html",
        title="Видалення допису",
        post=post
    )
