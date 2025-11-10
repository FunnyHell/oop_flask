import sqlite3, os
from flask import Flask, g


class Application:
    """
    Класс, собирающий всё приложение:
    — Создаём Flask,
    — подключаем БД,
    — регистрируем маршруты, обработчики
    """

    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "app.db")
        self.flask = self._build()

    def _build(self):
        ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
        STATIC_DIR = os.path.join(ROOT_DIR, "static")

        app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

        app.config["DATABASE"] = self.db_path
        app.config["SECRET_KEY"] = "dev"

        # Подключение
        app.before_request(self.open_db)
        app.teardown_appcontext(self.close_db)

        with app.app_context():
            self.init_schema()

        return app

    def open_db(self):
        if "_db" not in g:
            g._db = sqlite3.connect(self.db_path)
            g._db.row_factory = sqlite3.Row

    def close_db(self, _exc=None):
        db = g.pop("_db", None)
        if db is not None:
            db.close()

    def get_db(self):
        return g._db

    def init_schema(self):
        conn = sqlite3.connect(self.db_path)

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE SET NULL
            );
        """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                age INTEGER,
                email VARCHAR(255) NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sid_sha256 TEXT NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                last_seen  TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                revoked INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

        conn.commit()
        conn.close()
