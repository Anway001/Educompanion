from flask import Blueprint, request, jsonify, send_file, send_from_directory, current_app
from controllers.podcast_controller import handle_podcast_generation
# NEW: Import tools from Flask-JWT-Extended
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.saved_podcast import SavedPodcast
from config.database import db_instance
import uuid
import os, shutil, datetime

podcast_bp = Blueprint('podcast', __name__)

# --- DIRECTORY FOR SAVED PODCASTS ---
SAVED_PODCASTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'generated', 'saved_podcasts')
os.makedirs(SAVED_PODCASTS_DIR, exist_ok=True)
# ------------------------------------

# Initialize SavedPodcast model (MongoDB)
saved_podcast_model = SavedPodcast(db_instance.get_db())


@podcast_bp.route('/generate', methods=['POST'])
# MODIFIED: The generate endpoint should also be protected
@jwt_required()
def generate_podcast_endpoint():
    # ... your existing generate code is perfect, no changes needed inside ...
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
        send_path = result['path']
        if should_save:
            # Create a permanent path for the saved file
            # Use ObjectId-based storage; filename includes user id and timestamp
            timestamp = int(datetime.datetime.utcnow().timestamp())
            permanent_filename = f"{current_user_id}_{timestamp}_{result['filename']}"
            permanent_path = os.path.join(SAVED_PODCASTS_DIR, permanent_filename)
            shutil.move(result['path'], permanent_path) # Move from temp to permanent

            # Save metadata to MongoDB including the path
            meta_res = saved_podcast_model.create_saved_podcast_metadata(
                user_id=current_user_id,
                title=result['filename'],
                date=datetime.datetime.utcnow().isoformat(),
                preview=None,
                path=permanent_path
            )
            if not meta_res.get('success'):
                print(f"[WARN] Failed to save podcast metadata for user {current_user_id}: {meta_res}")
            # Update the path we'll send back to the client
            send_path = permanent_path

        return send_file(send_path, as_attachment=True, download_name=result['filename'])
    except Exception as e:
        print(f"[ERROR] in generate_podcast_endpoint: {e}")
        return jsonify({"error": "An unexpected server error occurred."}), 500


# MODIFIED: This route is now protected and filters by user
@podcast_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_podcasts():
    # Get the ID of the user who is making the request
    current_user_id = get_jwt_identity()
    print(f"[LOG] Request received to fetch podcasts for user: {current_user_id}")

    try:
        # Try querying by ObjectId first (common case when JWT stores ObjectId as string)
        from bson import ObjectId
        try:
            docs = list(saved_podcast_model.collection.find({"user_id": ObjectId(current_user_id)}))
        except Exception:
            # Fallback to string comparison if user_id stored as string
            docs = list(saved_podcast_model.collection.find({"user_id": str(current_user_id)}))
    except Exception:
        # If anything fails, return empty list
        docs = []

    # Clean documents for response
    filtered = []
    for d in docs:
        try:
            d['_id'] = str(d.get('_id'))
            d.pop('path', None)
            # Convert ObjectId user_id to string for client
            if d.get('user_id') is not None:
                d['user_id'] = str(d.get('user_id'))
            filtered.append(d)
        except Exception:
            continue

    return jsonify(filtered), 200


# MODIFIED: This route is now protected and saves the user's ID
@podcast_bp.route('/save', methods=['POST'])
@jwt_required()
def save_podcast_metadata():
    data = request.get_json()

    # Get the ID of the user who is saving the podcast
    current_user_id = get_jwt_identity()

    if not data or 'title' not in data:
        return jsonify({"error": "Missing title in request"}), 400

    res = saved_podcast_model.create_saved_podcast_metadata(
        user_id=current_user_id,
        title=data.get('title'),
        date=data.get('date'),
        preview=data.get('preview')
    )

    if res.get('success'):
        return jsonify({"message": "Podcast metadata saved successfully", "podcast_id": res.get('saved_podcast_id')}), 201
    else:
        return jsonify({"error": "Failed to save podcast metadata", "details": res.get('message')}), 500


# Authenticated download (attachment)
@podcast_bp.route('/download/<string:podcast_id>', methods=['GET'])
@jwt_required()
def download_podcast(podcast_id):
    current_user_id = get_jwt_identity()
    try:
        from bson import ObjectId
        doc = saved_podcast_model.collection.find_one({"_id": ObjectId(podcast_id)})
    except Exception:
        return jsonify({"error": "Invalid podcast id"}), 400

    if not doc:
        return jsonify({"error": "Podcast not found"}), 404

    if str(doc.get('user_id')) != str(current_user_id):
        return jsonify({"error": "Access denied"}), 403

    path = doc.get('path')
    if not path or not os.path.exists(path):
        return jsonify({"error": "Podcast file not found on server"}), 404

    filename = os.path.basename(path)
    return send_file(path, as_attachment=True, download_name=filename)


# Create a public share link (authenticated)
@podcast_bp.route('/share/<string:podcast_id>', methods=['POST'])
@jwt_required()
def share_podcast(podcast_id):
    current_user_id = get_jwt_identity()
    try:
        from bson import ObjectId
        doc = saved_podcast_model.collection.find_one({"_id": ObjectId(podcast_id)})
    except Exception:
        return jsonify({"error": "Invalid podcast id"}), 400

    if not doc:
        return jsonify({"error": "Podcast not found"}), 404

    if str(doc.get('user_id')) != str(current_user_id):
        return jsonify({"error": "Access denied"}), 403

    # create a token and expiry (7 days)
    token = str(uuid.uuid4())
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    try:
        saved_podcast_model.collection.update_one(
            {"_id": ObjectId(podcast_id)},
            {"$set": {"share_token": token, "share_expires": expires}}
        )
    except Exception as e:
        return jsonify({"error": "Failed to create share link", "details": str(e)}), 500

    # build share URL
    base = request.host_url.rstrip('/')
    share_url = f"{base}/api/podcast/shared/{token}"
    return jsonify({"share_url": share_url, "expires_at": expires.isoformat()}), 200


# Public shared access (no auth required)
@podcast_bp.route('/shared/<string:token>', methods=['GET'])
def shared_podcast(token):
    try:
        doc = saved_podcast_model.collection.find_one({"share_token": token})
    except Exception:
        return jsonify({"error": "Invalid token"}), 400

    if not doc:
        return jsonify({"error": "Shared podcast not found"}), 404

    expires = doc.get('share_expires')
    if not expires or expires < datetime.datetime.utcnow():
        return jsonify({"error": "Share link expired"}), 410

    path = doc.get('path')
    if not path or not os.path.exists(path):
        return jsonify({"error": "Podcast file not found on server"}), 404

    filename = os.path.basename(path)
    return send_file(path, as_attachment=True, download_name=filename)

# NEW: Route to stream a saved podcast
@podcast_bp.route('/play/<string:podcast_id>', methods=['GET'])
@jwt_required()
def play_podcast(podcast_id):
    current_user_id = get_jwt_identity()

    try:
        from bson import ObjectId
        doc = saved_podcast_model.collection.find_one({"_id": ObjectId(podcast_id)})
    except Exception:
        return jsonify({"error": "Invalid podcast id"}), 400

    if not doc:
        return jsonify({"error": "Podcast not found"}), 404

    if str(doc.get('user_id')) != str(current_user_id):
        return jsonify({"error": "Access denied"}), 403

    path = doc.get('path')
    if not path or not os.path.exists(path):
        return jsonify({"error": "Podcast file not found on server"}), 404

    return send_file(path, as_attachment=False)