from flask import Blueprint, request, jsonify
from controllers.summarizer_controller import handle_summarization

summarizer_bp = Blueprint('summarizer', __name__, url_prefix='/api/summarizer')

@summarizer_bp.route('/summarize', methods=['POST'])
def summarize_file():
    file = request.files.get('file')
    text = request.form.get('text')
    response, status = handle_summarization(file=file, text=text)
    return jsonify(response), status

