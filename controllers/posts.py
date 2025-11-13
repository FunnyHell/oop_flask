from flask import request, render_template, flash, redirect, url_for, g

from models.post import Post
from utils.decorators import login_required


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
        model.increment_views(post_id)
        post["views"] += 1
        return render_template(
            "posts/show.html", title=post["title"], post=post,
        )

    @login_required
    def create(self):
        if request.method == "GET":
            return render_template("/posts/create.html", title="Новый пост")
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        error = False
        if not title or not content:
            flash("Не заполнены все поля", "warning")
            error = True
        if len(title) < 5:
            flash("Заголовок должен быть не менее 5 символов", "warning")
            error = True
        if len(content) < 10:
            flash("Текст должен быть не менее 10 символов", "warning")
            error = True

        if error:
            return render_template(
                "/posts/create.html",
                title="Новый пост",
                form={"title": title, "content": content},
            )
        conn = self.get_db()
        model = Post(conn)

        author_id = g.user["id"] if hasattr(g, "user") and g.user else None

        post_id = model.create(title, content, author_id)
        return redirect(url_for("posts.show", post_id=post_id))

    @login_required
    def edit(self, post_id):
        conn = self.get_db()
        model = Post(conn)
        post = model.get(post_id)

        if not post:
            flash("Статья не найдена", "warning")
            return redirect(url_for("posts.index"))

        if post.get("author_id") != (g.user["id"] if hasattr(g, "user") and
                                                     g.user else None):
            flash("Вы не можете редактировать чужие статьи", "danger")
            return redirect(url_for("posts.show", post_id=post_id))

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

    @login_required
    def delete(self, post_id):
        conn = self.get_db()
        model = Post(conn)
        post = model.get(post_id)
        if not post:
            flash("Статья не найдена", "warning")
            return redirect(url_for("posts.index"))

        if post.get("author_id") != (g.user["id"] if hasattr(g, "user") and
                                                     g.user else None):
            flash("Вы не можете удалять чужие статьи", "danger")
            return redirect(url_for("posts.show", post_id=post_id))

        model.delete(post_id)
        flash("Пост удалён", "info")
        return redirect(url_for("posts.index"))
