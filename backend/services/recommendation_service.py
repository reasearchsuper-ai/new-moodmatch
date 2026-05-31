"""
MoodMatch Song Recommendation Engine
Advanced matching using emotion vectors + BPM/energy/valence alignment.
"""

import logging
from backend.models.songs_data import (
    get_songs_by_mood_profile, get_songs_by_emotion, get_song_by_id
)

logger = logging.getLogger(__name__)

# Emotion display names and metadata (defined here to avoid circular import)
EMOTION_META = {
    "happy":    {"label": "Happy",    "emoji": "😊", "color": "#FFD700", "valence": "positive"},
    "sad":      {"label": "Sad",      "emoji": "😢", "color": "#4A90D9", "valence": "negative"},
    "angry":    {"label": "Angry",    "emoji": "😠", "color": "#E74C3C", "valence": "negative"},
    "surprise": {"label": "Surprised","emoji": "😲", "color": "#FF8C00", "valence": "neutral"},
    "fear":     {"label": "Fearful",  "emoji": "😨", "color": "#9B59B6", "valence": "negative"},
    "disgust":  {"label": "Disgusted","emoji": "🤢", "color": "#27AE60", "valence": "negative"},
    "neutral":  {"label": "Calm",     "emoji": "😌", "color": "#85C1E9", "valence": "neutral"},
}

# Ideal energy/valence targets per mood
MOOD_AUDIO_PROFILE = {
    "happy":    {"energy": 0.80, "valence": 0.85, "bpm_range": (100, 170)},
    "sad":      {"energy": 0.25, "valence": 0.15, "bpm_range": (60, 95)},
    "angry":    {"energy": 0.90, "valence": 0.25, "bpm_range": (100, 160)},
    "surprise": {"energy": 0.85, "valence": 0.65, "bpm_range": (100, 155)},
    "fear":     {"energy": 0.35, "valence": 0.20, "bpm_range": (65, 100)},
    "disgust":  {"energy": 0.80, "valence": 0.25, "bpm_range": (100, 160)},
    "neutral":  {"energy": 0.35, "valence": 0.45, "bpm_range": (70, 110)},
}


class RecommendationEngine:

    def recommend(self, emotion_summary: dict, limit: int = 15) -> dict:
        primary = emotion_summary.get('primary_emotion', 'neutral')
        secondary = emotion_summary.get('secondary_emotion', 'neutral')
        emotion_scores = emotion_summary.get('emotion_scores', {})
        intensity = emotion_summary.get('mood_intensity', 'medium')

        logger.info(f"🎵 Generating recommendations for: {primary} ({intensity})")

        songs = get_songs_by_mood_profile(emotion_scores, limit=limit + 5)

        if len(songs) < limit:
            extras = get_songs_by_emotion(primary, limit=10)
            seen_ids = {s['id'] for s in songs}
            for s in extras:
                if s['id'] not in seen_ids:
                    songs.append(s)

        songs = self._apply_intensity_boost(songs, primary, intensity)
        songs = self._add_explanations(songs, primary, secondary, emotion_scores)
        songs = songs[:limit]

        for i, song in enumerate(songs):
            song['rank'] = i + 1

        return {
            "songs": songs,
            "total": len(songs),
            "primary_emotion": primary,
            "secondary_emotion": secondary,
            "mood_label": emotion_summary.get('mood_label', ''),
            "mood_message": emotion_summary.get('mood_message', ''),
            "playlist_title": self._generate_playlist_title(primary, intensity),
            "playlist_description": self._generate_playlist_desc(primary, emotion_scores),
        }

    def _apply_intensity_boost(self, songs, emotion, intensity):
        profile = MOOD_AUDIO_PROFILE.get(emotion, {})
        target_energy = profile.get('energy', 0.5)
        bpm_range = profile.get('bpm_range', (70, 130))

        for song in songs:
            boost = 0
            energy_diff = abs(song.get('energy', 0.5) - target_energy)
            boost += (1 - energy_diff) * 0.1

            bpm = song.get('bpm', 100)
            if bpm_range[0] <= bpm <= bpm_range[1]:
                boost += 0.05

            if intensity == 'high' and song.get('energy', 0) > 0.75:
                boost += 0.05
            elif intensity == 'low' and song.get('energy', 0) < 0.40:
                boost += 0.05

            song['match_score'] = round(song.get('match_score', 0) + boost, 4)

        songs.sort(key=lambda x: x['match_score'], reverse=True)
        return songs

    def _add_explanations(self, songs, primary, secondary, scores):
        for song in songs:
            reasons = []
            song_emotions = song.get('emotions', [])

            if primary in song_emotions:
                meta = EMOTION_META.get(primary, {})
                reasons.append(f"Matches your {meta.get('label', primary).lower()} mood")

            if secondary in song_emotions and secondary != primary:
                meta = EMOTION_META.get(secondary, {})
                reasons.append(f"Resonates with your {meta.get('label', secondary).lower()} undertone")

            energy = song.get('energy', 0.5)
            if energy > 0.8:
                reasons.append("High energy to fuel your vibe")
            elif energy < 0.3:
                reasons.append("Gentle sound to match your headspace")

            if song.get('valence', 0.5) > 0.8:
                reasons.append("Uplifting and positive")
            elif song.get('valence', 0.5) < 0.2:
                reasons.append("Deep emotional resonance")

            song['recommendation_reason'] = reasons[0] if reasons else "Great match for your mood"
            song['all_reasons'] = reasons

        return songs

    def _generate_playlist_title(self, emotion, intensity):
        titles = {
            "happy":   {"high": "Pure Joy Overdrive 🌟", "medium": "Sunshine Sessions ☀️", "low": "Gentle Smiles 😊"},
            "sad":     {"high": "Deep Feelings Archive 💙", "medium": "Quiet Afternoons 🌧", "low": "Soft Reflections ✨"},
            "angry":   {"high": "Controlled Explosion 🔥", "medium": "Raw Energy Channel ⚡", "low": "Simmering Power 💪"},
            "neutral": {"high": "Centered & Clear 🧘", "medium": "The Zen Zone 🌊", "low": "Still Waters 💫"},
            "surprise":{"high": "Maximum Hype 🚀", "medium": "Electric Feels ⚡", "low": "Pleasant Surprises 🎉"},
            "fear":    {"high": "Face Your Fears 🌙", "medium": "Gentle Courage 💙", "low": "Safe Harbour 🏠"},
            "disgust": {"high": "Rebellious Spirit 🤘", "medium": "Against the Grain 🎸", "low": "Just Not Feeling It 😤"},
        }
        return titles.get(emotion, {}).get(intensity, "Your MoodMatch Playlist 🎵")

    def _generate_playlist_desc(self, emotion, scores):
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        desc = f"Curated for your {emotion} mood with undertones of "
        desc += " and ".join([f"{e} ({round(s*100)}%)" for e, s in top if e != emotion])
        return desc + ". Enjoy the journey."


# Singleton
_engine = None

def get_recommendation_engine():
    global _engine
    if _engine is None:
        _engine = RecommendationEngine()
    return _engine