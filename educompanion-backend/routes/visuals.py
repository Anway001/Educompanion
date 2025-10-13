from flask import Blueprint, send_from_directory, jsonify
from controllers.visuals_controller import process_file_controller
import os
from urllib.parse import unquote

visuals_bp = Blueprint('visuals', __name__, url_prefix='/api/visuals')

# --- CONFIGURATION FOR SERVING GENERATED FILES ---
# The absolute path to the 'educompanion-backend' directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The absolute path to the directory where generated files are stored
GENERATED_DIR = os.path.join(BACKEND_DIR, 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)
# --------------------------------------------------

@visuals_bp.route('/generate', methods=['POST'])
def generate_visuals_endpoint():
    return process_file_controller()

# --- UPDATED: ROUTE TO SERVE GENERATED VISUALS ---
@visuals_bp.route('/generated/<path:filename>')
def serve_generated_file(filename):
    """Serves a file from the 'generated' directory."""
    try:
        # Decode %20, %2F, etc.
        decoded_filename = unquote(filename)
        full_path = os.path.join(GENERATED_DIR, decoded_filename)

        # Debug log (optional)
        print(f"Serving file: {full_path}")

        if not os.path.exists(full_path):
            return jsonify({"error": f"File not found: {decoded_filename}"}), 404

        return send_from_directory(GENERATED_DIR, decoded_filename)
    except Exception as e:
        print(f"❌ Error serving file: {e}")
        return jsonify({"error": str(e)}), 500
# --------------------------------------------------
