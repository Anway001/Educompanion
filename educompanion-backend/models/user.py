from datetime import datetime
import bcrypt
from bson import ObjectId

class User:
    def __init__(self, db):
        self.db = db
        self.collection = db.users
    
    def create_user(self, email, password, first_name, last_name):
        """Create a new user"""
        try:
            # Check if user already exists
            if self.collection.find_one({"email": email}):
                return {"success": False, "message": "User with this email already exists"}
            
            # Hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Create user document
            user_data = {
                "email": email,
                "password": hashed_password,
                "first_name": first_name,
                "last_name": last_name,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
            
            # Insert user into database
            result = self.collection.insert_one(user_data)
            
            if result.inserted_id:
                # Return user data without password
                user_data.pop('password')
                user_data['_id'] = str(result.inserted_id)
                return {"success": True, "user": user_data}
            else:
                return {"success": False, "message": "Failed to create user"}
                
        except Exception as e:
            return {"success": False, "message": f"Error creating user: {str(e)}"}
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            # Find user by email
            user = self.collection.find_one({"email": email})
            
            if not user:
                return {"success": False, "message": "Invalid email or password"}
            
            # Check if user is active
            if not user.get('is_active', True):
                return {"success": False, "message": "Account is deactivated"}
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Return user data without password
                user_data = {
                    "_id": str(user['_id']),
                    "email": user['email'],
                    "first_name": user['first_name'],
                    "last_name": user['last_name'],
                    "created_at": user['created_at'],
                    "updated_at": user['updated_at']
                }
                return {"success": True, "user": user_data}
            else:
                return {"success": False, "message": "Invalid email or password"}
                
        except Exception as e:
            return {"success": False, "message": f"Error authenticating user: {str(e)}"}
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
                user.pop('password', None)  # Remove password from response
                return {"success": True, "user": user}
            else:
                return {"success": False, "message": "User not found"}
        except Exception as e:
            return {"success": False, "message": f"Error getting user: {str(e)}"}
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        try:
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.utcnow()
            
            # Remove fields that shouldn't be updated
            update_data.pop('_id', None)
            update_data.pop('email', None)  # Don't allow email changes for now
            update_data.pop('created_at', None)
            
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return {"success": True, "message": "User updated successfully"}
            else:
                return {"success": False, "message": "No changes made"}
                
        except Exception as e:
            return {"success": False, "message": f"Error updating user: {str(e)}"}
    
    def delete_user(self, user_id):
        """Delete user (soft delete by setting is_active to False)"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                return {"success": True, "message": "User deleted successfully"}
            else:
                return {"success": False, "message": "User not found"}
                
        except Exception as e:
            return {"success": False, "message": f"Error deleting user: {str(e)}"}
