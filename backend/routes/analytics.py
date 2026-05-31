"""MoodMatch Analytics & History Routes"""

from flask import Blueprint, jsonify
from backend.models.database import get_global_analytics, get_all_sessions, get_emotion_summary, get_session

analytics_bp = Blueprint('analytics', __name__)
history_bp = Blueprint('history', __name__)


@analytics_bp.route('/analytics', methods=['GET'])
def analytics():
    data = get_global_analytics()
    return jsonify({"success": True, "data": data}), 200


@history_bp.route('/history', methods=['GET'])
def history():
    sessions = get_all_sessions(limit=50)
    enriched = []
    for s in sessions:
        summary = get_emotion_summary(s['id'])
        enriched.append({
            **s,
            "emotion_summary": summary
        })
    return jsonify({"success": True, "sessions": enriched, "total": len(enriched)}), 200


@history_bp.route('/session/<session_id>/full', methods=['GET'])
def session_full(session_id):
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Not found"}), 404
    summary = get_emotion_summary(session_id)
    return jsonify({
        "success": True,
        "session": session,
        "emotion_summary": summary
    }), 200