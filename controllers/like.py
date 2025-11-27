from flask import g, jsonify

from models.like import Like
from models.post import Post
from utils.decorators import login_required


class LikeController:
    """
    Контроллер для управления лайками.

    Работает с и возвращает JSON-данные
    Все операции кроме GET требуют авторизации.

    Attributes:
        get_db: sqlite3 connection
    """

    def __init__(self, get_db):
        self.get_db = get_db

    @login_required
    def add_like(self, post_id: int):
        """Add like to post

        :param post_id: ID of the post to like
        :type post_id: int

        :return: JSON response with success flag and like count
        :rtype: flask.Response

        **Example successful response**:

        .. code-block:: JSON

            {
                "success": true,
                "likes_count": 42
            }

        **Example error response**:

        .. code-block:: JSON

            {
                "success": false,
                "message": "Like already exists"
            }
        """
        conn = self.get_db()
        post_model = Post(conn)
        like_model = Like(conn)
        if not post_model.get(post_id):
            return jsonify({"success": False, "message": "Post not found"}), 404

        user_id = g.user["id"]

        success = like_model.add_like(user_id, post_id)
        if not success:
            return jsonify(
                {
                    "success": False, "message": "Like already exists",
                },
            ), 409

        likes_count = like_model.get_likes_count(post_id)
        return jsonify(
            {
                "success": True,
                "message": "ok",
                "likes_count": likes_count,
            },
        ), 201

    @login_required
    def remove_like(self, post_id: int):
        conn = self.get_db()
        post_model = Post(conn)
        like_model = Like(conn)
        if not post_model.get(post_id):
            return jsonify({"success": False, "message": "Post not found"}), 404

        user_id = g.user["id"]

        success = like_model.remove_like(user_id, post_id)
        if not success:
            return jsonify(
                {
                    "success": False, "message": "Like already removed",
                },
            ), 409

        likes_count = like_model.get_likes_count(post_id)
        return jsonify(
            {
                "success": True,
                "message": "ok",
                "likes_count": likes_count,
            },
        ), 201

    @login_required
    def toggle_like(self, post_id: int):
        conn = self.get_db()
        post_model = Post(conn)
        like_model = Like(conn)
        if not post_model.get(post_id):
            return jsonify({"success": False, "message": "Post not found"}), 404

        user_id = g.user["id"]

        success = like_model.toggle_like(user_id, post_id)

        if not success:
            return jsonify(
                {
                    "success": False, "message": "Error while updating like",
                },
            ), 409

        user_liked = like_model.has_liked(user_id, post_id)
        likes_count = like_model.get_likes_count(post_id)
        return jsonify(
            {
                "success": True,
                "message": "ok",
                "user_liked": user_liked,
                "likes_count": likes_count,
            },
        ), 200

    # TODO: Дописываем обязательный минимум методов для LikeController (API)
    #  → Refactor → Тесты/тестовые запросы
    def get_post_likes_info(self, post_id):
        conn = self.get_db()
        post_model = Post(conn)
        like_model = Like(conn)
        if not post_model.get(post_id):
            return jsonify({"success": False, "message": "Post not found"}), 404

        info = like_model.get_post_likes_info(post_id)

    #     TODO: get_post_likes_info в модели, должен вернуть
    #      {
    #      "info": get_users_who_likes(post_id),
    #      "likes_count": get_likes_count(post_id)
    #      }

    def get_likes_count(self):
        # TODO: return: {"success": True, "likes_count": N}
        #               {"success": False, "message": "Post not found"}
        pass

    def get_users_who_liked(self):
        # users = like_model.get_user_who_likes(post_id)
        # TODO: return: {"success": True,
        #               "users": [{"id": 1, ...}, {...},...],
        #               "count": N}
        #
        #               {"success": False, "message": "Post not found"}
        pass

    # ==========================================================================

    def get_user_likes(self):
        pass

    def check_like(self):
        pass
