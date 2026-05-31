"""MoodMatch Emotion API Routes"""

from flask import Blueprint, jsonify
from backend.models.database import get_emotion_summary, get_emotion_timeline, get_session

emotion_bp = Blueprint('emotion', __name__)


@emotion_bp.route('/emotions/<session_id>', methods=['GET'])
def get_emotions(session_id):
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    summary = get_emotion_summary(session_id)
    if not summary:
        return jsonify({"error": "Emotions not ready yet", "status": session['status']}), 202

    return jsonify({"success": True, "data": summary}), 200


@emotion_bp.route('/emotions/<session_id>/timeline', methods=['GET'])
def get_timeline(session_id):
    frames = get_emotion_timeline(session_id)
    if not frames:
        return jsonify({"error": "Timeline not available"}), 404

    # Build time range segments: group consecutive frames with same dominant emotion
    segments = []
    current_emotion = None
    segment_start = 0

    for i, frame in enumerate(frames):
        emotion = frame['dominant_emotion']
        time_sec = frame['timestamp_ms'] / 1000

        if emotion != current_emotion:
            # Close previous segment
            if current_emotion is not None:
                segments[-1]['end_sec'] = round(time_sec, 1)
                segments[-1]['label'] = f"{segments[-1]['start_sec']}s → {round(time_sec, 1)}s"

            # Start new segment
            segments.append({
                "emotion": emotion,
                "start_sec": round(time_sec, 1),
                "end_sec": None,
                "label": "",
                "frame_index": i
            })
            current_emotion = emotion

    # Close last segment
    if segments:
        last_time = frames[-1]['timestamp_ms'] / 1000
        segments[-1]['end_sec'] = round(last_time, 1)
        segments[-1]['label'] = f"{segments[-1]['start_sec']}s → {round(last_time, 1)}s"

    # Build chart-friendly format with from→to labels
    timeline = {
        "labels": [f"{f['timestamp_ms']/1000:.1f}s" for f in frames],
        "range_labels": [
            f"{f['timestamp_ms']/1000:.0f}s - {frames[i+1]['timestamp_ms']/1000:.0f}s"
            if i + 1 < len(frames)
            else f"{f['timestamp_ms']/1000:.0f}s - end"
            for i, f in enumerate(frames)
        ],
        "datasets": {
            "happy":   [f['happy'] for f in frames],
            "sad":     [f['sad'] for f in frames],
            "angry":   [f['angry'] for f in frames],
            "neutral": [f['neutral'] for f in frames],
            "surprise":[f['surprise'] for f in frames],
            "fear":    [f['fear'] for f in frames],
            "disgust": [f['disgust'] for f in frames],
        },
        "dominant": [f['dominant_emotion'] for f in frames],
        "segments": segments  # Time range blocks with from→to
    }

    return jsonify({"success": True, "timeline": timeline, "frames": frames}), 200