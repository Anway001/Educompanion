from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def chat_message():
    data = request.get_json() or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    user_id = get_jwt_identity()

    # Predefined Q&A map (case-insensitive keys)
    qa_map = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hello! How can I help you today?',
        'hey': 'Hello! How can I help you today?',
        'how do i create a podcast': 'To create a podcast: go to the Podcast page, upload or provide notes, then click Generate. You can save the generated podcast to your account.',
        'how to save a podcast': 'After generating, choose "Save" or use the Save button on the podcast player to store it in your account.',
        'how to share a podcast': 'Open the saved podcast and use the Share button to create a public link you can send to others. Note: only podcasts with files can be shared.',
        'how do i change my password': 'Go to Settings -> Account and use the change password form to update your password.',
        'what formats are supported': 'We currently support MP3 audio for podcasts. Video notes can be exported as MP4.'
    }

    normalized = message.lower()
    # Exact match first
    reply = qa_map.get(normalized)
    if not reply:
        # simple contains-based matching
        for k, v in qa_map.items():
            if k in normalized:
                reply = v
                break

    if not reply:
        reply = "Sorry, I don't have an exact answer for that yet. Try asking about creating, saving, or sharing podcasts."

    response = {
        'message': message,
        'reply': reply,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'user': user_id
    }

    return jsonify(response), 200


@chat_bp.route('/message_public', methods=['POST'])
def chat_message_public():
    """Public version of the chat endpoint for quick testing during development.
    It uses the same predefined Q&A map but does not require authentication.
    """
    data = request.get_json() or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    qa_map = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hello! How can I help you today?',
        'hey': 'Hello! How can I help you today?',
        'how do i create a podcast': 'To create a podcast: go to the Podcast page, upload or provide notes, then click Generate. You can save the generated podcast to your account.',
        'how to save a podcast': 'After generating, choose "Save" or use the Save button on the podcast player to store it in your account.',
        'how to share a podcast': 'Open the saved podcast and use the Share button to create a public link you can send to others. Note: only podcasts with files can be shared.',
        'how do i change my password': 'Go to Settings -> Account and use the change password form to update your password.',
        'what formats are supported': 'We currently support MP3 audio for podcasts. Video notes can be exported as MP4.'
    }

    normalized = message.lower()
    reply = qa_map.get(normalized)
    if not reply:
        for k, v in qa_map.items():
            if k in normalized:
                reply = v
                break

    if not reply:
        reply = "Sorry, I don't have an exact answer for that yet. Try asking about creating, saving, or sharing podcasts."

    response = {
        'message': message,
        'reply': reply,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    return jsonify(response), 200
