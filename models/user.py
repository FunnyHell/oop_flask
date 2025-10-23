import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        
    def create(self, name, age, email, password):
        pw_hash = generate_password_hash(password)
        cur = self.conn.execute(
            "INSERT INTO users(name, age, email, password) VALUES (?, ?, ?, ?)",
            [name, age, email, pw_hash]
        )
        self.conn.commit()
        return cur.lastrowid
    
    def find_by_email(self, email):
        cur = self.conn.execute("SELECT * FROM users WHERE email = ?", [email])
        row = cur.fetchone()
        return dict(row) if row else None
    
    def find_by_id(self, id):
        cur = self.conn.execute("SELECT * FROM users WHERE id = ?", [id])
        row = cur.fetchone()
        return dict(row) if row else None
    
    def verifty_password(self, user, raw_password):
        return check_password_hash(user["password"], raw_password)