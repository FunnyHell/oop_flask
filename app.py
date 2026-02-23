from datetime import datetime
import os, sqlite3

from extensions import socketio
from flask import redirect, url_for, request

from app_core.app import Application
from blueprints.auth import create_auth_blueprint
from blueprints.like import create_like_blueprint
from blueprints.posts import create_posts_blueprint
from controllers.auth import AuthController
from controllers.like import LikeController
from controllers.posts import PostsController
from models.comment import Comment

from models.session import SessionStore
from models.user import User

core = Application()
app = core.flask
socketio.init_app(app)

posts_controller = PostsController(core.get_db)
auth_controller = AuthController(core.get_db, session_ttl_minutes=60 * 24 * 7)
like_controller = LikeController(core.get_db)

app.register_blueprint(create_posts_blueprint(posts_controller))
app.register_blueprint(create_auth_blueprint(auth_controller))
app.register_blueprint(create_like_blueprint(like_controller))


@app.before_request
def load_user():
    auth_controller.load_user()


@app.route("/")
def home():
    return redirect(url_for('posts.index'))

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__name__), "app_core", "app.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_from_cookie(sid_cookie):
    if not sid_cookie:
        return None

    conn = get_db_connection()
    store = SessionStore(conn)
    session = store.get_valid(sid_cookie)

    user = None
    if session:
        user_model = User(conn)
        user = user_model.find_by_id(session['user_id'])
    conn.close()
    return user

# rooms - каждый пост имеет свою комнату, в которую будут заходить/выходить юзеры
@socketio.on("join_post")
def on_join_post(data):
    from flask_socketio import join_room, emit
    post_id = data.get('post_id')
    if not post_id:
        return

    room = f"post_{post_id}"
    join_room(room)

    conn = get_db_connection()
    comment_model = Comment(conn)
    comments = comment_model.get_by_post(post_id)
    conn.close()

    emit("initial_comments", {"comments": comments})

@socketio.on("add_comment")
def handle_add_comment(data):
    post_id = data.get("post_id")
    content = data.get("content", "").strip()
    sid = request.cookies.get("sid")

    if not content or not post_id:
        return

    user = get_user_from_cookie(sid)
    if not user:
        return

    conn = get_db_connection()
    comment_model = Comment(conn)

    new_comment_id = comment_model.create(content, post_id, user['id'])
    conn.close()

    comment_data = {
        "id": new_comment_id,
        "content": content,
        "post_id": post_id,
        "author_id": user['id'],
        "author_name": user['name'],
        "created_at": datetime.now().isoformat()
    }

    socketio.emit("new_comment", comment_data, to=f"post_{post_id}")

# @socketio.on("delete_comment")
if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
