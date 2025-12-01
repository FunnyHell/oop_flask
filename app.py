from flask import redirect, url_for
from app_core.app import Application
from blueprints.like import create_like_blueprint
from controllers.like import LikeController
from controllers.posts import PostsController
from blueprints.posts import create_posts_blueprint

from controllers.auth import AuthController
from blueprints.auth import create_auth_blueprint

core = Application()
app = core.flask

posts_controller = PostsController(core.get_db)
auth_controller = AuthController(core.get_db, session_ttl_minutes=60*24*7)
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
    app.run(debug=True)