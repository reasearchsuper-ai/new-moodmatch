"""
MoodMatch Upload API Route
Handles video file uploads with validation, progress tracking, and async processing.
"""

import os
import uuid
import threading
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from backend.models.database import (
    init_db, create_session, update_session_status,
    get_session, save_emotion_frames, save_emotion_summary, save_recommendations
)
from backend.services.emotion_service import get_detector
from backend.services.recommendation_service import get_recommendation_engine

logger = logging.getLogger(__name__)
upload_bp = Blueprint('upload', __name__)

# Initialize DB on first import
init_db()


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def process_video_async(app, session_id, filepath):
    """
    Background thread: run emotion detection + recommendation generation.
    Updates DB status throughout.
    """
    with app.app_context():
        try:
            logger.info(f"[{session_id}] Starting background processing")
            update_session_status(session_id, 'analyzing')

            # 1. Emotion detection
            detector = get_detector()
            result = detector.analyze_video(filepath, session_id)

            # 2. Save frames to DB
            save_emotion_frames(session_id, result['frames'])

            # 3. Save summary
            summary = result['summary']
            summary['frames_analyzed'] = result['video_metadata']['frames_analyzed']
            save_emotion_summary(session_id, summary)

            # 4. Generate recommendations
            engine = get_recommendation_engine()
            recs = engine.recommend(summary, limit=15)
            save_recommendations(session_id, recs['songs'])

            # 5. Mark complete
            update_session_status(
                session_id, 'completed',
                duration=result['video_metadata']['duration_seconds']
            )
            logger.info(f"[{session_id}] ✅ Processing complete")

        except Exception as e:
            logger.error(f"[{session_id}] ❌ Processing failed: {e}", exc_info=True)
            update_session_status(session_id, 'failed', error=str(e))


@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    """
    POST /api/upload
    Accept a video file, start async processing, return session_id.
    """
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided", "code": "NO_FILE"}), 400

    file = request.files['video']
    if not file or file.filename == '':
        return jsonify({"error": "Empty filename", "code": "EMPTY_FILE"}), 400

    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'mp4', 'avi', 'mov', 'mkv', 'webm'})
    if not allowed_file(file.filename, allowed):
        return jsonify({
            "error": f"Unsupported file type. Allowed: {', '.join(allowed)}",
            "code": "INVALID_TYPE"
        }), 400

    # Generate session
    session_id = str(uuid.uuid4())
    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower()
    stored_filename = f"{session_id}.{ext}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, stored_filename)

    # Save file
    file.save(filepath)
    file_size = os.path.getsize(filepath)
    logger.info(f"📁 Saved: {stored_filename} ({file_size/1024/1024:.1f} MB)")

    # Create DB session
    create_session(session_id, stored_filename, original_name, file_size)

    # Launch background processing
    app = current_app._get_current_object()
    thread = threading.Thread(
        target=process_video_async,
        args=(app, session_id, filepath),
        daemon=True
    )
    thread.start()

    return jsonify({
        "success": True,
        "session_id": session_id,
        "filename": original_name,
        "file_size_mb": round(file_size / 1024 / 1024, 2),
        "status": "processing",
        "message": "Video uploaded! Analyzing your emotions..."
    }), 202


@upload_bp.route('/status/<session_id>', methods=['GET'])
def get_status(session_id):
    """
    GET /api/status/<session_id>
    Poll for processing status.
    """
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    status = session['status']
    response = {
        "session_id": session_id,
        "status": status,
        "filename": session.get('original_name', ''),
        "created_at": session.get('created_at', ''),
    }

    if status == 'completed':
        response['completed_at'] = session.get('completed_at', '')
        response['duration_seconds'] = session.get('duration_seconds', 0)
        response['redirect_url'] = f"/playlist/{session_id}"
    elif status == 'failed':
        response['error'] = session.get('error_message', 'Unknown error')

    return jsonify(response), 200