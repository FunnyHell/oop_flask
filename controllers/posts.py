from flask import request, render_template, flash, redirect, url_for
from models.post import Post


class PostsController:
    """
    Контроллер не знает ни об app | g
    Он получает функции, возвращает соединения
    """

    def __init__(self, get_db):
        self.get_db = get_db

    def index(self):
        conn = self.get_db()
        model = Post(conn)
        items = model.all()
        return render_template("posts/index.html", title="Посты", items=items)

    def show(self, post_id):
        conn = self.get_db()
        model = Post(conn)
        post = model.get(post_id)
        if not post:
            return render_template("errors/404.html", title="Не найдено")
        return render_template("posts/show.html", title=post["title"], post=post)

    def create(self):
        if request.method == "GET":
            return render_template("/posts/create.html", title="Новый пост")
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        if not title or not content:
            flash("Не заполнены все поля", "warning")
            return render_template(
                "/posts/create.html",
                title="Новый пост",
                form={"title": title, "content": content},
            )
        conn = self.get_db()
        model = Post(conn)
        post_id = model.create(title, content)
        return redirect(url_for("posts.show", post_id = post_id))

    def edit(self, post_id):
        conn = self.get_db()
        model = Post(conn)
        post = model.get(post_id)

        if request.method == "GET":
            return render_template(
                "/posts/update.html",
                title=f"Редактирование: {post['title']}",
                post=post,
            )
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        if not title or not content:
            flash("Не заполнены все поля", "warning")
            return render_template(
                "/posts/update.html",
                title=f"Редактирование: {post['title']}",
                post=post,
            )
        model.update(post_id, title, content)
        flash("Пост успешно обновлён", "success")
        return redirect(url_for('posts.show', post_id=post_id))
        
    def delete(self, post_id):
        conn = self.get_db()
        model = Post(conn)
        if not model.get(post_id):
            return render_template("errors/404.html", title="Не найдено")
        model.delete(post_id)
        flash("Пост удалён", "info")
        return redirect(url_for("posts.index"))