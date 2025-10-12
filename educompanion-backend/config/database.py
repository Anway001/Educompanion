from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            # Get MongoDB URI from environment variables
            mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            db_name = os.getenv('MONGODB_DB', 'educompanion')
            
            # Create MongoDB client
            self.client = MongoClient(mongo_uri)
            
            # Test the connection
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB!")
            
            # Get database
            self.db = self.client[db_name]
            
            # Create collections if they don't exist
            self._create_collections()
            
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            return False
    
    def _create_collections(self):
        """Create necessary collections if they don't exist"""
        collections = ['users', 'sessions', 'files']
        
        for collection_name in collections:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
                print(f"✅ Created collection: {collection_name}")
    
    def get_db(self):
        """Get database instance"""
        return self.db
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")

# Global database instance
db_instance = Database()
