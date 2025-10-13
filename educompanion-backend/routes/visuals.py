from flask import Blueprint, send_from_directory
from controllers.visuals_controller import process_file_controller
import os

visuals_bp = Blueprint('visuals', __name__)

# --- CONFIGURATION FOR SERVING GENERATED FILES ---
# The absolute path to the 'educompanion-backend' directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The absolute path to the directory where generated files are stored
GENERATED_DIR = os.path.join(BACKEND_DIR, 'generated')
# --------------------------------------------------

@visuals_bp.route('/generate', methods=['POST'])
def generate_visuals_endpoint():
    return process_file_controller()

# --- NEW: ROUTE TO SERVE GENERATED VISUALS ---
@visuals_bp.route('/generated/<path:filename>')
def serve_generated_file(filename):
    """Serves a file from the 'generated' directory."""
    # The 'send_from_directory' function needs the directory path and the filename.
    # It will then locate and serve the requested file.
    # This is a secure way to provide file access from a specific directory.
    return send_from_directory(GENERATED_DIR, filename)
# --------------------------------------------
