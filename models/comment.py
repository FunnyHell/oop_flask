import sqlite3


class Comment:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create(self, content, post_id, author_id):
        cur = self.conn.execute(
            """
            INSERT INTO comments (content, post_id, author_id)
            VALUES (?, ?, ?)
            """,
            [content, post_id, author_id],
        )
        self.conn.commit()
        return cur.lastrowid

    def get_by_post(self, post_id):
        cur = self.conn.execute(
            """
            SELECT c.id,
                   c.content,
                   c.author_id,
                   c.post_id,
                   c.created_at,
                   u.name AS author_name
            FROM comments c
                     JOIN
                 users u ON c.author_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
            """, [post_id],
        )
        return [dict(row) for row in cur.fetchall()]

    def get_by_id(self, comment_id):
        cur = self.conn.execute(
            """
            SELECT c.id,
                   c.content,
                   c.author_id,
                   c.post_id,
                   c.created_at,
                   u.name AS author_name
            FROM comments c
                     JOIN
                 users u ON c.author_id = u.id
            WHERE c.id = ?
            """, [comment_id],
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def delete(self, comment_id):
        cur = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        return cur.rowcount > 0
