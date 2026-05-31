"""MoodMatch Songs & Recommendations API Routes"""

from flask import Blueprint, jsonify, request
from backend.models.database import (
    get_emotion_summary, get_recommendations, get_session, log_interaction
)
from backend.models.songs_data import get_all_songs, get_song_by_id, get_songs_by_emotion
from backend.services.recommendation_service import get_recommendation_engine

songs_bp = Blueprint('songs', __name__)


@songs_bp.route('/recommendations/<session_id>', methods=['GET'])
def get_session_recommendations(session_id):
    """Get full recommendations for a session"""
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    if session['status'] != 'completed':
        return jsonify({"status": session['status'], "message": "Still processing..."}), 202

    summary = get_emotion_summary(session_id)
    if not summary:
        return jsonify({"error": "Emotion data missing"}), 404

    # Get stored recommendation IDs
    stored = get_recommendations(session_id)
    stored_ids = [r['song_id'] for r in stored]

    # Rebuild full song objects
    engine = get_recommendation_engine()
    recs = engine.recommend(summary, limit=15)

    return jsonify({
        "success": True,
        "session_id": session_id,
        "recommendations": recs,
        "emotion_summary": summary
    }), 200


@songs_bp.route('/songs', methods=['GET'])
def list_songs():
    """List all songs in the database"""
    emotion_filter = request.args.get('emotion')
    if emotion_filter:
        songs = get_songs_by_emotion(emotion_filter)
    else:
        songs = get_all_songs()
    return jsonify({"songs": songs, "total": len(songs)}), 200


@songs_bp.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = get_song_by_id(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    return jsonify({"song": song}), 200


@songs_bp.route('/interact', methods=['POST'])
def interact():
    """Log user interaction with a song (like, skip, play)"""
    data = request.get_json()
    session_id = data.get('session_id')
    song_id = data.get('song_id')
    action = data.get('action')  # 'like', 'skip', 'play'

    if not all([session_id, song_id, action]):
        return jsonify({"error": "Missing fields"}), 400

    if action not in ['like', 'skip', 'play']:
        return jsonify({"error": "Invalid action"}), 400

    log_interaction(session_id, song_id, action)
    return jsonify({"success": True}), 200