from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure Flask
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.podcast import podcast_bp # Ensure this is the correct path to your blueprint
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(podcast_bp, url_prefix='/api/podcast')
    
    # Basic route for testing
    @app.route('/')
    def home():
        return {'message': 'EduCompanion Backend API is running!'}
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Backend is working correctly!'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080)) # Matching port to your previous logs
    
    # MODIFIED: Added use_reloader=False to prevent conflicts with multiprocessing.
    app.run(host=host, port=port, debug=True, use_reloader=False)