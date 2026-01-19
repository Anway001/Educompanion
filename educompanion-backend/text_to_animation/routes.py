"""
Text-to-Animation API Routes
Defines Flask routes for the text-to-animation functionality
"""

from flask import Blueprint, request, jsonify
from .controller import controller

# Create blueprint
text_to_animation_bp = Blueprint('text_to_animation', __name__)

# Routes

@text_to_animation_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload file for text-to-animation processing"""
    return controller.upload_file()

@text_to_animation_bp.route('/process/<file_id>', methods=['POST'])
def process_file(file_id):
    """Process uploaded file and generate video"""
    return controller.process_file(file_id)

@text_to_animation_bp.route('/status/<file_id>', methods=['GET'])
def get_processing_status(file_id):
    """Get processing status for a file"""
    return controller.get_processing_status(file_id)

@text_to_animation_bp.route('/download/<video_id>', methods=['GET'])
def download_video(video_id):
    """Download generated video file"""
    return controller.download_video(video_id)

@text_to_animation_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'text-to-animation',
        'message': 'Text-to-animation service is running'
    })
