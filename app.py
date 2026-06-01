"""
MoodMatch - AI-Powered Emotion-to-Music App
Entry point for the Flask application
"""

import os

# Must be before any other imports
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')

from flask import Flask, render_template
from flask_cors import CORS
from backend.routes.upload import upload_bp
from backend.routes.emotion import emotion_bp
from backend.routes.songs import songs_bp
from backend.routes.analytics import analytics_bp
from backend.routes.history import history_bp
from flask import Flask

# The variable MUST be named exactly 'app'
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'moodmatch-secret-2024')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max upload
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'}
    app.config['DATABASE'] = os.path.join(os.getcwd(), 'moodmatch.db')

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(emotion_bp, url_prefix='/api')
    app.register_blueprint(songs_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    app.register_blueprint(history_bp, url_prefix='/api')

    # Frontend routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/history')
    def history_page():
        return render_template('history.html')

    @app.route('/playlist/<session_id>')
    def playlist(session_id):
        return render_template('playlist.html', session_id=session_id)

    # Health check for Render
    @app.route('/health')
    def health():
        return {"status": "ok"}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    print("🎵 MoodMatch is running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
