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
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.podcast import podcast_bp
    from routes.visuals import visuals_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(podcast_bp, url_prefix='/api/podcast')
    app.register_blueprint(visuals_bp, url_prefix='/api/visuals')

    print("Registered Blueprints:")
    for bp_name, bp in app.blueprints.items():
        print(f"- {bp_name} at {bp.url_prefix}")
    
    # Basic route for testing
    @app.route('/')
    def home():
        return {'message': 'EduCompanion Backend API is running!'}
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Backend is working correctly!'}
    
    return app
