
from datetime import datetime

from flask import render_template, redirect, url_for, flash, abort, request

from . import post_bp
from .models import Post
from .forms import PostForm
from app.extensions import db


# Створення нового допису
@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data or datetime.utcnow()
        )

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

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data or post.posted

        db.session.commit()

        flash("Допис успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted

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
