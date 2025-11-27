import sqlite3


class Like:
    """
    Класс для работы с лайками постов
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_like(self, user_id: int, post_id: int):
        try:
            self.conn.execute(
                "INSERT INTO likes(user_id, post_id) VALUES (?, ?)",
                [user_id, post_id], )
            self.conn.execute(
                "UPDATE posts SET likes = likes + 1 WHERE id = ?", [post_id],
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            print(f"Лайк уже существует: {e}")
            return False
        except sqlite3.OperationalError as e:
            self.conn.rollback()
            print(f"Ошибка БД: {e}")
            return False

    def remove_like(self, user_id: int, post_id: int):
        if self.has_liked(user_id, post_id):
            self.conn.execute(
                "DELETE FROM likes WHERE user_id = ? AND post_id = ?",
                [user_id, post_id],
            )
            self.conn.execute(
                "UPDATE posts SET likes = likes - 1 WHERE id = ?", [post_id],
            )
            self.conn.commit()
            return True
        return False

    def toggle_like(self, user_id: int, post_id: int):
        if self.has_liked(user_id, post_id):
            return self.remove_like(user_id, post_id)
        return self.add_like(user_id, post_id)

    def get_likes_count(self, post_id):
        cur = self.conn.execute(
            "SELECT COUNT(*) as count FROM likes WHERE post_id = ?",
            [post_id],
        )
        row = cur.fetchone()
        return row["count"] if row else 0

    def get_users_who_likes(self, post_id, limit=10):
    # likes → l user → u.id, u.name, l.created_at
        cur = self.conn.execute(
            """
            SELECT u.id, u.name. l.created_at
            FROM likes l
            JOIN users u ON u.id = l.user_id
            WHERE l.post_id = ?
            ORDER BY l.created_at DESC 
            LIMIT ?
            """
        )
        row = cur.fetchall()
        return row

    def has_liked(self, user_id: int, post_id: int):
        cur = self.conn.execute(
            "SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?",
            [user_id, post_id],
        )
        return cur.fetchone() is not None