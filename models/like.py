import sqlite3

class Like:
    """
    Класс для работы с лайками постов
    """
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_like(self, user_id: int, post_id: int):
        pass

    def remove_like(self, user_id: int, post_id: int):
        pass

    def get_likes_count(self, post_id):
        pass

    def get_user_who_likes(self, post_id, limit=10):
        pass

    def has_liked(self, user_id: int, post_id: int):
        pass
