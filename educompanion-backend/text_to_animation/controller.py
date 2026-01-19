"""
Text-to-Animation API Controller
Handles file upload, processing, and video generation
"""

import os
import uuid
import tempfile
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
from pathlib import Path

# Import the text-to-animation pipeline
from .pipeline import run_pipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextToAnimationController:
    """Controller for text-to-animation operations"""

    def __init__(self):
        self.upload_folder = 'educompanion-backend/uploads'
        self.output_folder = 'educompanion-backend/generated'
        self.temp_dir = 'educompanion-backend/text_to_animation/ttm_tmp'

        # Create directories if they don't exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def upload_file(self):
        """Handle file upload for text-to-animation processing"""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'pdf'}
            if not self._allowed_file(file.filename, allowed_extensions):
                return jsonify({'error': 'File type not supported. Use PNG, JPG, JPEG, or PDF'}), 400

            # Generate unique filename
            file_extension = Path(file.filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(self.upload_folder, unique_filename)

            # Save file
            file.save(file_path)
            logger.info(f"File saved: {file_path}")

            return jsonify({
                'message': 'File uploaded successfully',
                'file_id': unique_filename,
                'file_path': file_path
            }), 200

        except Exception as e:
            logger.error(f"Upload error: {e}")
            return jsonify({'error': str(e)}), 500

    def process_file(self, file_id):
        """Process uploaded file and generate video"""
        try:
            # Find the uploaded file
            file_path = None
            for filename in os.listdir(self.upload_folder):
                if filename.startswith(file_id):
                    file_path = os.path.join(self.upload_folder, filename)
                    break

            if not file_path or not os.path.exists(file_path):
                return jsonify({'error': 'File not found'}), 404

            # Generate output video path
            output_filename = f"{uuid.uuid4()}_animation.mp4"
            output_path = os.path.join(self.output_folder, output_filename)

            logger.info(f"Processing file: {file_path} -> {output_path}")

            # Run the text-to-animation pipeline
            run_pipeline(file_path, output_path)

            if not os.path.exists(output_path):
                return jsonify({'error': 'Video generation failed'}), 500

            return jsonify({
                'message': 'Video generated successfully',
                'video_id': output_filename,
                'video_path': output_path,
                'download_url': f'/api/text-to-animation/download/{output_filename}'
            }), 200

        except Exception as e:
            logger.error(f"Processing error: {e}")
            return jsonify({'error': str(e)}), 500

    def download_video(self, video_id):
        """Download generated video file"""
        try:
            video_path = os.path.join(self.output_folder, video_id)

            if not os.path.exists(video_path):
                return jsonify({'error': 'Video not found'}), 404

            return send_file(video_path, as_attachment=True)

        except Exception as e:
            logger.error(f"Download error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_processing_status(self, file_id):
        """Get processing status for a file"""
        try:
            # Check if video already exists for this file
            for filename in os.listdir(self.output_folder):
                if filename.startswith(file_id) and filename.endswith('_animation.mp4'):
                    return jsonify({
                        'status': 'completed',
                        'video_id': filename,
                        'download_url': f'/api/text-to-animation/download/{filename}'
                    }), 200

            # Check if file exists in uploads
            file_exists = False
            for filename in os.listdir(self.upload_folder):
                if filename.startswith(file_id):
                    file_exists = True
                    break

            if not file_exists:
                return jsonify({'error': 'File not found'}), 404

            return jsonify({'status': 'processing'}), 200

        except Exception as e:
            logger.error(f"Status check error: {e}")
            return jsonify({'error': str(e)}), 500

    def _allowed_file(self, filename, allowed_extensions):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Create controller instance
controller = TextToAnimationController()
