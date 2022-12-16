from flask import Blueprint
from controllers.AuthControllers import login, logout, post_login

auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.route('/login', methods=['GET'])(login)
auth_blueprint.route('/login', methods=['POST'])(post_login)
auth_blueprint.route('/logout', methods=['GET'])(logout)

