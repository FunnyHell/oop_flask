from flask import Blueprint

from controllers.like import LikeController


def create_like_blueprint(controller: LikeController):
    bp = Blueprint("like", __name__, url_prefix="/api/like")

    bp.add_url_rule(
        "/<int:post_id>", "add_like", controller.add_like, methods=["POST"],
    )
    bp.add_url_rule(
        "/<int:post_id>", "remove_like", controller.remove_like,
        methods=["DELETE"],
    )
    bp.add_url_rule(
        "/<int:post_id>", "check_like", controller.check_like, methods=["GET"],
    )
    bp.add_url_rule(
        "/<int:post_id>", "toggle_like", controller.toggle_like, methods=[
            "UPDATE",
        ],
    )
    bp.add_url_rule(
        "/<int:post_id>/count", "get_likes_count",
        controller.get_likes_count, methods=["GET"],
    )
    bp.add_url_rule(
        "/<int:post_id>", "get_post_likes_info", controller.get_post_likes_info,
        methods=["GET"],
    )
    return bp
