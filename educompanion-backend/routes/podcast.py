from flask import Blueprint, request, jsonify, send_file, send_from_directory
from controllers.podcast_controller import handle_podcast_generation
# NEW: Import tools from Flask-JWT-Extended
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

podcast_bp = Blueprint('podcast', __name__)

# --- TEMPORARY IN-MEMORY DATABASE ---
# This list will now store dictionaries that include a 'user_id'
saved_podcasts_db = []
next_id = 1
# ------------------------------------


@podcast_bp.route('/generate', methods=['POST'])
# MODIFIED: The generate endpoint should also be protected
@jwt_required()
def generate_podcast_endpoint():
    # ... your existing generate code is perfect, no changes needed inside ...
    notes_text = request.form.get('notes_text')
    file = request.files.get('file') or request.files.get('file ')
    podcast_length = request.form.get('length', 'medium').lower()

    if not notes_text and not file:
        return jsonify({"error": "No input data provided."}), 400

    try:
        result, status_code = handle_podcast_generation(
            notes_text=notes_text, file=file, length=podcast_length
        )
        if status_code != 200:
            return jsonify(result), status_code
        
        return send_file(result['path'], as_attachment=True, download_name=result['filename'])
    except Exception as e:
        return jsonify({"error": "An unexpected server error occurred."}), 500


# MODIFIED: This route is now protected and filters by user
@podcast_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_podcasts():
    # NEW: Get the ID of the user who is making the request
    current_user_id = get_jwt_identity()
    print(f"[LOG] Request received to fetch podcasts for user: {current_user_id}")
    
    # NEW: Filter the database to only include podcasts from the current user
    user_podcasts = [p for p in saved_podcasts_db if p.get('user_id') == current_user_id]
    
    return jsonify(user_podcasts), 200


# MODIFIED: This route is now protected and saves the user's ID
@podcast_bp.route('/save', methods=['POST'])
@jwt_required()
def save_podcast_metadata():
    global next_id
    data = request.get_json()
    
    # NEW: Get the ID of the user who is saving the podcast
    current_user_id = get_jwt_identity()

    if not data or 'title' not in data:
        return jsonify({"error": "Missing title in request"}), 400
    
    new_podcast = {
        "id": next_id,
        "user_id": current_user_id, # NEW: Tag the data with the user's ID
        "title": data.get('title'),
        "date": data.get('date'),
        "preview": data.get('preview')
    }
    
    saved_podcasts_db.append(new_podcast)
    next_id += 1
    
    print(f"[LOG] Saved new podcast metadata for user {current_user_id}: {new_podcast['title']}")
    return jsonify({"message": "Podcast metadata saved successfully", "podcast": new_podcast}), 201