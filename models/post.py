import sqlite3


class Post:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ---------CRUD-----------
    def all(self):
        cur = self.conn.execute("SELECT * FROM posts")
        return [dict(r) for r in cur.fetchall()]

    def get(self, post_id):
        cur = self.conn.execute("SELECT * FROM posts WHERE id = ?", [post_id])
        row = cur.fetchone()
        return dict(row) if row else None

    def create(self, title, content):
        cur = self.conn.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)", [title, content]
        )
        self.conn.commit()
        return cur.lastrowid

    def update(self, post_id, title, content):
        cur = self.conn.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            [title, content, post_id],
        )
        self.conn.commit()
        return self.get(post_id) if cur.rowcount else None

    def delete(self, post_id):
        cur = self.conn.execute("DELETE FROM posts WHERE id = ?", [post_id])
        self.conn.commit()
        return cur.rowcount > 0
