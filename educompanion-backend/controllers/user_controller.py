# controllers/user_controller.py
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User
from config.database import db_instance

user_model = User(db_instance.get_db())


class UserController:
    @staticmethod
    def update_profile(data):
        try:
            current_user_id = get_jwt_identity()

            # Validate data
            if not data:
                return jsonify({'success': False, 'message': 'No data provided for update'}), 400

            # Only allow updating specific fields
            allowed_fields = ['first_name', 'last_name']
            update_data = {}

            for field in allowed_fields:
                if field in data and data[field]:
                    if len(data[field].strip()) < 2:
                        return jsonify({
                            'success': False,
                            'message': f'{field} must be at least 2 characters long'
                        }), 400
                    update_data[field] = data[field].strip()

            if not update_data:
                return jsonify({'success': False, 'message': 'No valid fields to update'}), 400

            # Update user
            result = user_model.update_user(current_user_id, update_data)

            if result['success']:
                return jsonify({'success': True, 'message': result['message']}), 200
            else:
                return jsonify({'success': False, 'message': result['message']}), 400

        except Exception as e:
            return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

    @staticmethod
    def delete_profile():
        try:
            current_user_id = get_jwt_identity()
            result = user_model.delete_user(current_user_id)

            if result['success']:
                return jsonify({'success': True, 'message': result['message']}), 200
            else:
                return jsonify({'success': False, 'message': result['message']}), 400

        except Exception as e:
            return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

    @staticmethod
    def change_password(data):
        try:
            current_user_id = get_jwt_identity()

            if not data.get('current_password') or not data.get('new_password'):
                return jsonify({
                    'success': False,
                    'message': 'Current password and new password are required'
                }), 400

            new_password = data['new_password']

            if len(new_password) < 6:
                return jsonify({
                    'success': False,
                    'message': 'New password must be at least 6 characters long'
                }), 400

            user_result = user_model.get_user_by_id(current_user_id)
            if not user_result['success']:
                return jsonify({'success': False, 'message': 'User not found'}), 404

            # To be implemented later
            return jsonify({
                'success': False,
                'message': 'Password change feature will be implemented in the next phase'
            }), 501

        except Exception as e:
            return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
