from flask import Blueprint
from controllers.posts import PostsController

def create_posts_blueprint(controller: PostsController):
    bp = Blueprint("posts", __name__, url_prefix="/posts")
    
    bp.add_url_rule("/", "index", controller.index, methods=["GET"])
    bp.add_url_rule("/<int:post_id>", "show", controller.show, methods=["GET"])
    bp.add_url_rule("/create", "create", controller.create, methods=["GET", "POST"])
    bp.add_url_rule("/<int:post_id>/edit", "edit", controller.edit, methods=["GET", "POST"])
    bp.add_url_rule("/<int:post_id>/delete", "delete", controller.delete, methods=["POST"])


    return bp