from flask import Blueprint, request, jsonify
from controllers.summarizer_controller import handle_summarization

summarizer_bp = Blueprint('summarizer', __name__, url_prefix='/api/summarizer')

@summarizer_bp.route('/summarize', methods=['POST'])
def summarize_file():
    file = request.files.get('file')
    text = request.form.get('text')
    youtube_url = request.form.get('youtube_url')
    response, status = handle_summarization(file=file, text=text, youtube_url=youtube_url)
    return jsonify(response), status
