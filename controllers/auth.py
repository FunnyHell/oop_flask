from flask import request, render_template, redirect, url_for, flash, g, make_response
from models.user import User
from models.session import SessionStore

COOKIE_NAME = "sid"

class AuthController:
    def __init__(self, get_db, session_ttl_minutes = 60 * 24 * 7):
        self.get_db = get_db
        self.session_ttl_minutes = session_ttl_minutes
        
    def load_user(self):
        g.user = None
        sid = request.cookies.get(COOKIE_NAME)
        
        if sid:
            conn = self.get_db()
            store = SessionStore(conn, self.session_ttl_minutes)
            user_id = store.get_valid(sid)
            
            if user_id:
                user_id = user_id.get("user_id")
                model = User(conn)
                user = model.find_by_id(user_id)
                if user:
                    g.user = user
        return redirect(url_for('posts.index'))
        
    def register(self):
        if request.method == "GET":
            return render_template("users/register.html", title="Регистрация")

        name = (request.form.get("name") or "").strip()
        age_raw = (request.form.get("age") or "").strip()
        age = int(age_raw) if age_raw.isdigit() else None
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()
    
        if not name or not age or not email or not password:
            flash("Указаны не все данные", "warning")
            return redirect(url_for("auth.register"))
        
        conn = self.get_db()
        model = User(conn)
        
        if model.find_by_email(email):
            flash("Пользователь с таким email уже существует", "warning")
            return redirect(url_for("auth.register"))
        
        user_id = model.create(name, age, email, password)
        store = SessionStore(conn, self.session_ttl_minutes)
        sid, max_age = store.create(user_id)
        resp = make_response(redirect(url_for("auth.profile")))
        resp.set_cookie(COOKIE_NAME, sid, max_age=int(max_age), httponly=True, samesite="Lax")
        return resp
        
    def login(self):
        if request.method == "GET":
            return render_template("users/login.html", title="Вход")

        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()
        
        conn = self.get_db()
        model = User(conn)
        user = model.find_by_email(email)
        
        if not user or not model.verifty_password(user, password):
            flash("Неверные email или пароль", "danger")
            return redirect("auth/login")
        
        store = SessionStore(conn, self.session_ttl_minutes)
        sid, max_age = store.create(user["id"])
        resp = make_response(redirect(url_for("auth.profile")))
        resp.set_cookie(COOKIE_NAME, sid, max_age=int(max_age), httponly=True, samesite="Lax")
        return resp
        
    def profile(self):
        if not getattr(g, "user", None):
            return redirect(url_for("auth.login"))
        return render_template("users/profile.html", title="Профиль", user = g.user)
    
    def logout(self):
        sid = request.cookies.get(COOKIE_NAME)
        if sid:
            conn = self.get_db()
            SessionStore(conn).revoke_sid(sid)

        resp = make_response(redirect(url_for("home")))
        resp.delete_cookie(COOKIE_NAME)
        flash("Вы вышли из аккаунта", "info")
        return resp
    
    def logout_all(self):
        if not getattr(g, "user", None):
            return redirect(url_for("auth.login"))
        conn = self.get_db()
        SessionStore(conn).revoke_all_users(g.user["id"])
        
        resp = make_response(redirect(url_for("home")))
        resp.delete_cookie(COOKIE_NAME)
        flash("Вы завершили все сессии", "info")
        return resp
