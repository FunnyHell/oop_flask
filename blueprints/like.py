from flask import Blueprint
from controllers.like import LikeController


def create_like_blueprint(controller: LikeController):
    bp = Blueprint("like", __name__, url_prefix="/api/like")

    bp.add_url_rule("/<int:post_id>", "add_like", controller.add_like, methods=["POST"])
    return bp