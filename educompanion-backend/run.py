from app import create_app
from config.database import db_instance
from flask_cors import CORS
import os

def main():
    """Main function to run the application"""
    print("🚀 Starting EduCompanion Backend...")
    
    # Connect to database
    print("📡 Connecting to MongoDB...")
    if not db_instance.connect():
        print("❌ Failed to connect to MongoDB. Please check your connection settings.")
        return
    
    # Create Flask app
    app = create_app()

    
    CORS(app)
    
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Starting server on {host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("✅ Server is running! Press Ctrl+C to stop.")
    
    try:
        # Run the application
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        # Close database connection
        db_instance.close()

if __name__ == '__main__':
    main()
