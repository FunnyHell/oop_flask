from flask import redirect, url_for
from extensions import socketio

from app_core.app import Application
from blueprints.auth import create_auth_blueprint
from blueprints.like import create_like_blueprint
from blueprints.posts import create_posts_blueprint
from controllers.auth import AuthController
from controllers.like import LikeController
from controllers.posts import PostsController

core = Application()
app = core.flask
socketio.init_app(app)

@socketio.on("join_post")
def on_join(data):
    pass

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


if __name__ == "__main__":
    socketio.run(app, debug=True)
