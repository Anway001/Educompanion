from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from config.database import db_instance
import re

# Initialize User model with db
user_model = User(db_instance.get_db())

def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400

        email = data['email'].lower().strip()
        password = data['password']
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()

        # Validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 chars'}), 400
        if len(first_name) < 2 or len(last_name) < 2:
            return jsonify({'success': False, 'message': 'First and last name must be >= 2 chars'}), 400

        result = user_model.create_user(email, password, first_name, last_name)
        if result['success']:
            return jsonify({'success': True, 'message': 'User created', 'user': result['user']}), 201
        return jsonify({'success': False, 'message': result['message']}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Email and password required'}), 400

        email = data['email'].lower().strip()
        password = data['password']

        result = user_model.authenticate_user(email, password)
        if result['success']:
            access_token = create_access_token(identity=result['user']['_id'])
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': result['user'],
                'access_token': access_token
            }), 200
        return jsonify({'success': False, 'message': result['message']}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        result = user_model.get_user_by_id(current_user_id)
        if result['success']:
            return jsonify({'success': True, 'user': result['user']}), 200
        return jsonify({'success': False, 'message': result['message']}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@jwt_required()
def logout():
    """Logout endpoint (JWT handled client-side)"""
    return jsonify({'success': True, 'message': 'Logout successful'}), 200
