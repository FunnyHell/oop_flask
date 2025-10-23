from flask import Blueprint
from controllers.auth import AuthController

def create_auth_blueprint(controller: AuthController):
    bp = Blueprint("auth", __name__, url_prefix="/auth")
    
    bp.add_url_rule("/register", "register", controller.register, methods=["GET", "POST"])
    bp.add_url_rule("/login", "login", controller.login, methods=["GET", "POST"])
    bp.add_url_rule("/profile", "profile", controller.profile, methods=["GET"])
    bp.add_url_rule("/logout", "logout", controller.logout, methods=["POST"])
    bp.add_url_rule("/logout_all", "logout_all", controller.logout_all, methods=["POST"])

    return bp