from flask import Blueprint, request, jsonify, send_file, send_from_directory
from controllers.podcast_controller import handle_podcast_generation
# NEW: Import tools from Flask-JWT-Extended
from flask_jwt_extended import jwt_required, get_jwt_identity
import os, shutil, datetime

podcast_bp = Blueprint('podcast', __name__)

# --- DIRECTORY FOR SAVED PODCASTS ---
SAVED_PODCASTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'generated', 'saved_podcasts')
os.makedirs(SAVED_PODCASTS_DIR, exist_ok=True)
# ------------------------------------

# --- TEMPORARY IN-MEMORY DATABASE ---
# This list will now store dictionaries that include a 'user_id' and file path
saved_podcasts_db = []
next_id = 1
# ------------------------------------


@podcast_bp.route('/generate', methods=['POST'])
# MODIFIED: The generate endpoint should also be protected
@jwt_required()
def generate_podcast_endpoint():
    # ... your existing generate code is perfect, no changes needed inside ...
    global next_id
    current_user_id = get_jwt_identity()
    notes_text = request.form.get('notes_text')
    file = request.files.get('file') or request.files.get('file ')
    podcast_length = request.form.get('length', 'medium').lower()
    # NEW: Check if the user wants to save the podcast
    should_save = request.form.get('save', 'false').lower() == 'true'

    if not notes_text and not file:
        return jsonify({"error": "No input data provided."}), 400

    try:
        result, status_code = handle_podcast_generation(
            notes_text=notes_text, file=file, length=podcast_length
        )

        if status_code != 200:
            return jsonify(result), status_code

        # NEW: Save the podcast if requested
        if should_save:
            # Create a permanent path for the saved file
            permanent_filename = f"{current_user_id}_{next_id}_{result['filename']}"
            permanent_path = os.path.join(SAVED_PODCASTS_DIR, permanent_filename)
            shutil.move(result['path'], permanent_path) # Move from temp to permanent

            # Save metadata to our in-memory DB
            new_podcast = {
                "id": next_id,
                "user_id": current_user_id,
                "title": result['filename'], # Using filename as title, can be changed
                "date": datetime.datetime.now().isoformat(),
                "path": permanent_path # Store the path to the file
            }
            saved_podcasts_db.append(new_podcast)
            next_id += 1
            print(f"[LOG] Saved new podcast for user {current_user_id}: {permanent_filename}")

        return send_file(result['path'], as_attachment=True, download_name=result['filename'])
    except Exception as e:
        print(f"[ERROR] in generate_podcast_endpoint: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500


# MODIFIED: This route is now protected and filters by user
@podcast_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_podcasts():
    # NEW: Get the ID of the user who is making the request
    current_user_id = get_jwt_identity()
    print(f"[LOG] Request received to fetch podcasts for user: {current_user_id}")
    
    # NEW: Filter the database to only include podcasts from the current user
    # We remove the 'path' from the response for security/cleanliness
    user_podcasts = [
        {k: v for k, v in p.items() if k != 'path'} for p in saved_podcasts_db if p.get('user_id') == current_user_id
    ]
    
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

# NEW: Route to stream a saved podcast
@podcast_bp.route('/play/<int:podcast_id>', methods=['GET'])
@jwt_required()
def play_podcast(podcast_id):
    current_user_id = get_jwt_identity()
    
    # Find the podcast in the database
    podcast_to_play = next((p for p in saved_podcasts_db if p['id'] == podcast_id), None)

    # Check if the podcast exists and belongs to the current user
    if not podcast_to_play or podcast_to_play.get('user_id') != current_user_id:
        return jsonify({"error": "Podcast not found or access denied"}), 404

    # Check if the file exists on disk
    if not os.path.exists(podcast_to_play['path']):
        return jsonify({"error": "Podcast file not found on server"}), 404

    return send_file(podcast_to_play['path'], as_attachment=False)