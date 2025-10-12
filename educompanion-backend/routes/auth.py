from flask import Blueprint
from controllers.auth_controller import signup, login, get_profile, logout

auth_bp = Blueprint('auth', __name__)

# delegate requests to controller functions
auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/profile', methods=['GET'])(get_profile)
auth_bp.route('/logout', methods=['POST'])(logout)
