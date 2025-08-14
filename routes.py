# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Post

main = Blueprint("main", __name__)

@main.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

@main.route("/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]

        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_post.html")

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        post.author = request.form["author"]
        db.session.commit()
        flash("Post updated successfully!", "info")
        return redirect(url_for("main.index"))

    return render_template("edit_post.html", post=post)

@main.route("/delete/<int:id>")
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "danger")
    return redirect(url_for("main.index"))

@main.route("/api/posts", methods=["GET"])
def api_get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.author,
            "created_at": p.created_at
        } for p in posts
    ])

@main.route("/api/posts", methods=["POST"])
def api_create_post():
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "content", "author")):
        return jsonify({"error": "Missing fields"}), 400

    new_post = Post(
        title=data["title"],
        content=data["content"],
        author=data["author"]
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201

@main.route("/api/posts/<int:id>", methods=["PUT"])
def api_update_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.author = data.get("author", post.author)
    db.session.commit()
    return jsonify({"message": "Post updated successfully"}), 200

@main.route("/api/posts/<int:id>", methods=["DELETE"])
def api_delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200
