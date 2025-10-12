# routes/user.py
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    return UserController.update_profile(data)


@user_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    return UserController.delete_profile()


@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    return UserController.change_password(data)
