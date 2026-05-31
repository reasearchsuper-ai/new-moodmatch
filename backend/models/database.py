"""
MoodMatch Database Layer
SQLite database for storing sessions, emotion results, and analytics
"""

import sqlite3
import json
import os
from datetime import datetime


def get_db_path():
    return os.path.join(os.getcwd(), 'moodmatch.db')


def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize all database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Sessions table - each video upload is a session
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            original_name TEXT,
            file_size INTEGER,
            duration_seconds REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            error_message TEXT
        )
    ''')

    # Emotion results per frame
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_frames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            frame_number INTEGER,
            timestamp_ms REAL,
            dominant_emotion TEXT,
            happy REAL DEFAULT 0,
            sad REAL DEFAULT 0,
            angry REAL DEFAULT 0,
            surprise REAL DEFAULT 0,
            fear REAL DEFAULT 0,
            disgust REAL DEFAULT 0,
            neutral REAL DEFAULT 0,
            face_confidence REAL DEFAULT 0,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    ''')

    # Session emotion summary
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            primary_emotion TEXT,
            secondary_emotion TEXT,
            emotion_scores TEXT,
            mood_label TEXT,
            mood_intensity TEXT,
            faces_detected INTEGER DEFAULT 0,
            frames_analyzed INTEGER DEFAULT 0,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    ''')

    # Song recommendations per session
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            song_id TEXT NOT NULL,
            match_score REAL,
            emotion_match TEXT,
            position INTEGER,
            liked INTEGER DEFAULT 0,
            skipped INTEGER DEFAULT 0,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    ''')

    # User interactions (likes, skips, plays)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            song_id TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")


# ─── Session CRUD ────────────────────────────────────────────────────────────

def create_session(session_id, filename, original_name, file_size):
    conn = get_connection()
    conn.execute(
        'INSERT INTO sessions (id, filename, original_name, file_size, status) VALUES (?, ?, ?, ?, ?)',
        (session_id, filename, original_name, file_size, 'processing')
    )
    conn.commit()
    conn.close()


def update_session_status(session_id, status, error=None, duration=None):
    conn = get_connection()
    if status == 'completed':
        conn.execute(
            'UPDATE sessions SET status=?, completed_at=?, duration_seconds=? WHERE id=?',
            (status, datetime.now().isoformat(), duration, session_id)
        )
    elif status == 'failed':
        conn.execute(
            'UPDATE sessions SET status=?, error_message=? WHERE id=?',
            (status, error, session_id)
        )
    else:
        conn.execute('UPDATE sessions SET status=? WHERE id=?', (status, session_id))
    conn.commit()
    conn.close()


def get_session(session_id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM sessions WHERE id=?', (session_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_sessions(limit=50):
    conn = get_connection()
    rows = conn.execute(
        'SELECT s.*, es.primary_emotion, es.mood_label FROM sessions s '
        'LEFT JOIN emotion_summaries es ON s.id = es.session_id '
        'ORDER BY s.created_at DESC LIMIT ?', (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Emotion CRUD ─────────────────────────────────────────────────────────────

def save_emotion_frames(session_id, frames):
    conn = get_connection()
    for frame in frames:
        conn.execute('''
            INSERT INTO emotion_frames 
            (session_id, frame_number, timestamp_ms, dominant_emotion, happy, sad, angry, surprise, fear, disgust, neutral, face_confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            frame.get('frame_number', 0),
            frame.get('timestamp_ms', 0),
            frame.get('dominant_emotion', 'neutral'),
            frame.get('happy', 0),
            frame.get('sad', 0),
            frame.get('angry', 0),
            frame.get('surprise', 0),
            frame.get('fear', 0),
            frame.get('disgust', 0),
            frame.get('neutral', 0),
            frame.get('face_confidence', 0)
        ))
    conn.commit()
    conn.close()


def save_emotion_summary(session_id, summary):
    conn = get_connection()
    conn.execute('''
        INSERT OR REPLACE INTO emotion_summaries 
        (session_id, primary_emotion, secondary_emotion, emotion_scores, mood_label, mood_intensity, faces_detected, frames_analyzed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        session_id,
        summary['primary_emotion'],
        summary.get('secondary_emotion', ''),
        json.dumps(summary['emotion_scores']),
        summary.get('mood_label', ''),
        summary.get('mood_intensity', 'medium'),
        summary.get('faces_detected', 0),
        summary.get('frames_analyzed', 0)
    ))
    conn.commit()
    conn.close()


def get_emotion_summary(session_id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM emotion_summaries WHERE session_id=?', (session_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d['emotion_scores'] = json.loads(d['emotion_scores'])
        return d
    return None


def get_emotion_timeline(session_id):
    conn = get_connection()
    rows = conn.execute(
        'SELECT * FROM emotion_frames WHERE session_id=? ORDER BY frame_number',
        (session_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Recommendations CRUD ─────────────────────────────────────────────────────

def save_recommendations(session_id, songs):
    conn = get_connection()
    for i, song in enumerate(songs):
        conn.execute('''
            INSERT INTO recommendations (session_id, song_id, match_score, emotion_match, position)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, song['id'], song.get('match_score', 0), song.get('emotion_match', ''), i))
    conn.commit()
    conn.close()


def get_recommendations(session_id):
    conn = get_connection()
    rows = conn.execute(
        'SELECT * FROM recommendations WHERE session_id=? ORDER BY position',
        (session_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def log_interaction(session_id, song_id, action):
    conn = get_connection()
    conn.execute(
        'INSERT INTO interactions (session_id, song_id, action) VALUES (?, ?, ?)',
        (session_id, song_id, action)
    )
    if action == 'like':
        conn.execute(
            'UPDATE recommendations SET liked=1 WHERE session_id=? AND song_id=?',
            (session_id, song_id)
        )
    elif action == 'skip':
        conn.execute(
            'UPDATE recommendations SET skipped=1 WHERE session_id=? AND song_id=?',
            (session_id, song_id)
        )
    conn.commit()
    conn.close()


# ─── Analytics ────────────────────────────────────────────────────────────────

def get_global_analytics():
    conn = get_connection()

    total_sessions = conn.execute(
        'SELECT COUNT(*) as count FROM sessions WHERE status="completed"'
    ).fetchone()['count']

    emotion_dist = conn.execute('''
        SELECT primary_emotion, COUNT(*) as count 
        FROM emotion_summaries 
        GROUP BY primary_emotion 
        ORDER BY count DESC
    ''').fetchall()

    top_emotions = conn.execute('''
        SELECT dominant_emotion, COUNT(*) as count
        FROM emotion_frames
        GROUP BY dominant_emotion
        ORDER BY count DESC
        LIMIT 7
    ''').fetchall()

    conn.close()

    return {
        'total_sessions': total_sessions,
        'emotion_distribution': [dict(r) for r in emotion_dist],
        'top_emotions': [dict(r) for r in top_emotions]
    }