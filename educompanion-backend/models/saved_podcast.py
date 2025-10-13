from datetime import datetime
from bson import ObjectId

class SavedPodcast:
    def __init__(self, db):
        self.db = db
        self.collection = db.saved_podcasts

    def create_saved_podcast(self, user_id, title, file_path):
        """Create a new saved podcast"""
        try:
            saved_podcast_data = {
                "user_id": ObjectId(user_id),
                "title": title,
                "file_path": file_path,
                "created_at": datetime.utcnow()
            }
            
            result = self.collection.insert_one(saved_podcast_data)
            
            if result.inserted_id:
                return {"success": True, "saved_podcast_id": str(result.inserted_id)}
            else:
                return {"success": False, "message": "Failed to save podcast"}
                
        except Exception as e:
            return {"success": False, "message": f"Error saving podcast: {str(e)}"}

    def get_saved_podcasts_by_user(self, user_id):
        """Get all saved podcasts for a user"""
        try:
            podcasts = self.collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
            return {"success": True, "podcasts": list(podcasts)}
        except Exception as e:
            return {"success": False, "message": f"Error getting saved podcasts: {str(e)}"}

    def delete_saved_podcast(self, saved_podcast_id, user_id):
        """Delete a saved podcast"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(saved_podcast_id), "user_id": ObjectId(user_id)})
            if result.deleted_count > 0:
                return {"success": True, "message": "Podcast deleted successfully"}
            else:
                return {"success": False, "message": "Podcast not found or you don't have permission to delete it"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting podcast: {str(e)}"}

    def create_saved_podcast_metadata(self, user_id, title, date=None, preview=None, path=None):
        """Create a saved podcast entry (can include file path)

        Args:
            user_id: string user id
            title: title string
            date: ISO date string or None
            preview: preview text
            path: absolute file path to the saved audio file (optional)
        """
        try:
            podcast_data = {
                "user_id": ObjectId(user_id),
                "title": title,
                "preview": preview,
                "date": date,
                "path": path,
                "created_at": datetime.utcnow()
            }

            result = self.collection.insert_one(podcast_data)
            if result.inserted_id:
                return {"success": True, "saved_podcast_id": str(result.inserted_id)}
            else:
                return {"success": False, "message": "Failed to save podcast metadata"}
        except Exception as e:
            return {"success": False, "message": f"Error saving podcast metadata: {str(e)}"}
