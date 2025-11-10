import sqlite3


class Post:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ---------CRUD-----------
    def all(self):
        cur = self.conn.execute(
            """
            SELECT posts.id,
                   posts.title,
                   posts.content,
                   posts.views,
                   posts.likes,
                   posts.created_at,
                   posts.updated_at,
                   posts.author_id,
                   users.name
            FROM posts
                     JOIN users ON users.id = posts.author_id
            """,
        )
        return [dict(r) for r in cur.fetchall()]

    def get(self, post_id):
        cur = self.conn.execute(
            """SELECT *
               FROM posts
               WHERE id = ?""", [post_id],
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def create(self, title, content, author_id=None):
        cur = self.conn.execute(
            """
            INSERT
            INTO posts(title, content, author_id)
            VALUES (?, ?, ?) """,
            [title, content, author_id],
        )
        self.conn.commit()
        return cur.lastrowid

    def update(self, post_id, title, content):
        cur = self.conn.execute(
            """
            UPDATE
                posts
            SET title      = ?,
                content    = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            [title, content, post_id],
        )
        self.conn.commit()
        return self.get(post_id) if cur.rowcount else None

    def delete(self, post_id):
        cur = self.conn.execute(
            """DELETE
               FROM posts
               WHERE id = ?""", [post_id],
        )
        self.conn.commit()
        return cur.rowcount > 0

    def increment_views(self, post_id):
        cur = self.conn.execute(
            """
            UPDATE posts
            SET views = views + 1
            WHERE id = ?
            """,
            [post_id],
        )

        self.conn.commit()
        return cur.rowcount > 0


def get_by_author(self, author_id):
    cur = self.conn.execute(
        """
        SELECT *
        FROM posts
        WHERE author_id = ?
        """,
        [author_id],
    )
    return [dict(r) for r in cur.fetchall()]


def search(self, query):
    search_term = f"%{query}%"
    cur = self.conn.execute(
        """
        SELECT *
        FROM posts
        WHERE title LIKE ?
           OR content LIKE ?
        """,
        [search_term, search_term],
    )
    return [dict(r) for r in cur.fetchall()]


def get_top_viewed(self, limit=10):
    '''
    Вернуть какое-то количество самых популярных статей (10, 15, ...)
    '''
    cur = self.conn.execute(
        """
        SELECT *
        FROM posts
        ORDER BY views DESC LIMIT ?
        """, [limit],
    )
    return [dict(r) for r in cur.fetchall()]


def count_all(self):
    '''
    Возвращает кол-во статей на сайте
    '''
    cur = self.conn.execute("SELECT COUNT(*) as count FROM posts")
    row = cur.fetchone()
    return row["count"] if row else 0
