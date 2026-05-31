"""
MoodMatch Song Dataset
Rich curated collection of songs mapped to emotions and moods.
In production, replace with Spotify API / Apple Music integration.
"""

SONGS = [
    # ═══════════════════════════════════════════
    # HAPPY / JOYFUL
    # ═══════════════════════════════════════════
    {
        "id": "h001", "title": "Happy", "artist": "Pharrell Williams",
        "album": "G I R L", "year": 2013, "genre": "Pop/Soul",
        "duration": "3:53", "bpm": 160, "energy": 0.96, "valence": 0.96,
        "emotions": ["happy"], "mood_tags": ["euphoric", "upbeat", "positive"],
        "preview_url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH",
        "cover": "https://i.scdn.co/image/ab67616d0000b273e8107e6d9214baa81bb79bba",
        "color": "#FFD700"
    },
    {
        "id": "h002", "title": "Can't Stop the Feeling!", "artist": "Justin Timberlake",
        "album": "Trolls OST", "year": 2016, "genre": "Pop/Funk",
        "duration": "3:56", "bpm": 113, "energy": 0.85, "valence": 0.94,
        "emotions": ["happy"], "mood_tags": ["dance", "fun", "upbeat"],
        "preview_url": "", "cover": "", "color": "#FF6B35"
    },
    {
        "id": "h003", "title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars",
        "album": "Uptown Special", "year": 2014, "genre": "Funk/Pop",
        "duration": "4:30", "bpm": 115, "energy": 0.92, "valence": 0.88,
        "emotions": ["happy"], "mood_tags": ["dance", "groove", "fun"],
        "preview_url": "", "cover": "", "color": "#FF4500"
    },
    {
        "id": "h004", "title": "Good as Hell", "artist": "Lizzo",
        "album": "Cuz I Love You", "year": 2019, "genre": "Pop/Soul",
        "duration": "2:39", "bpm": 95, "energy": 0.79, "valence": 0.91,
        "emotions": ["happy"], "mood_tags": ["empowering", "positive", "feel-good"],
        "preview_url": "", "cover": "", "color": "#FF69B4"
    },
    {
        "id": "h005", "title": "Shake It Off", "artist": "Taylor Swift",
        "album": "1989", "year": 2014, "genre": "Pop",
        "duration": "3:39", "bpm": 160, "energy": 0.90, "valence": 0.94,
        "emotions": ["happy"], "mood_tags": ["carefree", "dance", "positive"],
        "preview_url": "", "cover": "", "color": "#FF1493"
    },
    {
        "id": "h006", "title": "Levitating", "artist": "Dua Lipa",
        "album": "Future Nostalgia", "year": 2020, "genre": "Pop/Disco",
        "duration": "3:23", "bpm": 103, "energy": 0.82, "valence": 0.82,
        "emotions": ["happy", "surprise"], "mood_tags": ["euphoric", "dance", "dreamy"],
        "preview_url": "", "cover": "", "color": "#9B59B6"
    },
    {
        "id": "h007", "title": "Blinding Lights", "artist": "The Weeknd",
        "album": "After Hours", "year": 2019, "genre": "Synth-pop",
        "duration": "3:20", "bpm": 171, "energy": 0.82, "valence": 0.33,
        "emotions": ["happy", "neutral"], "mood_tags": ["energetic", "night", "drive"],
        "preview_url": "", "cover": "", "color": "#E74C3C"
    },
    {
        "id": "h008", "title": "Don't Start Now", "artist": "Dua Lipa",
        "album": "Future Nostalgia", "year": 2019, "genre": "Nu-Disco",
        "duration": "3:27", "bpm": 124, "energy": 0.79, "valence": 0.66,
        "emotions": ["happy"], "mood_tags": ["empowering", "dance", "confident"],
        "preview_url": "", "cover": "", "color": "#3498DB"
    },
    {
        "id": "h009", "title": "Watermelon Sugar", "artist": "Harry Styles",
        "album": "Fine Line", "year": 2020, "genre": "Pop/Rock",
        "duration": "2:54", "bpm": 95, "energy": 0.78, "valence": 0.88,
        "emotions": ["happy"], "mood_tags": ["summer", "feel-good", "chill"],
        "preview_url": "", "cover": "", "color": "#27AE60"
    },
    {
        "id": "h010", "title": "Walking on Sunshine", "artist": "Katrina and The Waves",
        "album": "Walking on Sunshine", "year": 1985, "genre": "Pop/Rock",
        "duration": "3:58", "bpm": 109, "energy": 0.94, "valence": 0.97,
        "emotions": ["happy"], "mood_tags": ["classic", "euphoric", "summer"],
        "preview_url": "", "cover": "", "color": "#F39C12"
    },

    # ═══════════════════════════════════════════
    # SAD / MELANCHOLIC
    # ═══════════════════════════════════════════
    {
        "id": "s001", "title": "Someone Like You", "artist": "Adele",
        "album": "21", "year": 2011, "genre": "Soul/Pop",
        "duration": "4:45", "bpm": 68, "energy": 0.25, "valence": 0.06,
        "emotions": ["sad"], "mood_tags": ["heartbreak", "longing", "emotional"],
        "preview_url": "", "cover": "", "color": "#2C3E50"
    },
    {
        "id": "s002", "title": "The Night We Met", "artist": "Lord Huron",
        "album": "Strange Trails", "year": 2015, "genre": "Indie Folk",
        "duration": "3:28", "bpm": 82, "energy": 0.27, "valence": 0.11,
        "emotions": ["sad"], "mood_tags": ["nostalgic", "melancholy", "longing"],
        "preview_url": "", "cover": "", "color": "#1A252F"
    },
    {
        "id": "s003", "title": "Skinny Love", "artist": "Bon Iver",
        "album": "For Emma, Forever Ago", "year": 2007, "genre": "Indie Folk",
        "duration": "3:58", "bpm": 89, "energy": 0.19, "valence": 0.10,
        "emotions": ["sad"], "mood_tags": ["heartbreak", "raw", "acoustic"],
        "preview_url": "", "cover": "", "color": "#2E4057"
    },
    {
        "id": "s004", "title": "Fix You", "artist": "Coldplay",
        "album": "X&Y", "year": 2005, "genre": "Alternative Rock",
        "duration": "4:55", "bpm": 138, "energy": 0.33, "valence": 0.25,
        "emotions": ["sad"], "mood_tags": ["comforting", "hopeful-sad", "emotional"],
        "preview_url": "", "cover": "", "color": "#154360"
    },
    {
        "id": "s005", "title": "Motion Picture Soundtrack", "artist": "Radiohead",
        "album": "Kid A", "year": 2000, "genre": "Art Rock",
        "duration": "7:01", "bpm": 70, "energy": 0.09, "valence": 0.08,
        "emotions": ["sad"], "mood_tags": ["ethereal", "somber", "cinematic"],
        "preview_url": "", "cover": "", "color": "#0D1117"
    },
    {
        "id": "s006", "title": "When the Party's Over", "artist": "Billie Eilish",
        "album": "When We All Fall Asleep", "year": 2018, "genre": "Pop",
        "duration": "3:16", "bpm": 74, "energy": 0.17, "valence": 0.18,
        "emotions": ["sad"], "mood_tags": ["melancholy", "intimate", "quiet"],
        "preview_url": "", "cover": "", "color": "#17202A"
    },
    {
        "id": "s007", "title": "Liability", "artist": "Lorde",
        "album": "Melodrama", "year": 2017, "genre": "Art Pop",
        "duration": "3:42", "bpm": 81, "energy": 0.17, "valence": 0.09,
        "emotions": ["sad"], "mood_tags": ["vulnerable", "raw", "piano"],
        "preview_url": "", "cover": "", "color": "#212F3D"
    },
    {
        "id": "s008", "title": "Hurt", "artist": "Johnny Cash",
        "album": "American IV", "year": 2002, "genre": "Country/Alternative",
        "duration": "3:38", "bpm": 83, "energy": 0.22, "valence": 0.05,
        "emotions": ["sad"], "mood_tags": ["regret", "haunting", "powerful"],
        "preview_url": "", "cover": "", "color": "#0B0C0C"
    },
    {
        "id": "s009", "title": "The Sound of Silence", "artist": "Simon & Garfunkel",
        "album": "Wednesday Morning, 3 A.M.", "year": 1964, "genre": "Folk",
        "duration": "3:05", "bpm": 78, "energy": 0.14, "valence": 0.07,
        "emotions": ["sad"], "mood_tags": ["classic", "loneliness", "poetic"],
        "preview_url": "", "cover": "", "color": "#1C2833"
    },
    {
        "id": "s010", "title": "Crying in the Club", "artist": "Camila Cabello",
        "album": "Camila", "year": 2017, "genre": "Pop/R&B",
        "duration": "3:43", "bpm": 80, "energy": 0.59, "valence": 0.31,
        "emotions": ["sad", "happy"], "mood_tags": ["bittersweet", "emotional"],
        "preview_url": "", "cover": "", "color": "#4A235A"
    },

    # ═══════════════════════════════════════════
    # ANGRY / INTENSE
    # ═══════════════════════════════════════════
    {
        "id": "a001", "title": "HUMBLE.", "artist": "Kendrick Lamar",
        "album": "DAMN.", "year": 2017, "genre": "Hip-Hop",
        "duration": "2:57", "bpm": 150, "energy": 0.89, "valence": 0.42,
        "emotions": ["angry"], "mood_tags": ["aggressive", "power", "confident"],
        "preview_url": "", "cover": "", "color": "#C0392B"
    },
    {
        "id": "a002", "title": "Break Stuff", "artist": "Limp Bizkit",
        "album": "Significant Other", "year": 1999, "genre": "Nu-Metal",
        "duration": "2:46", "bpm": 115, "energy": 0.96, "valence": 0.30,
        "emotions": ["angry"], "mood_tags": ["rage", "cathartic", "intense"],
        "preview_url": "", "cover": "", "color": "#922B21"
    },
    {
        "id": "a003", "title": "Killing in the Name", "artist": "Rage Against the Machine",
        "album": "Rage Against the Machine", "year": 1992, "genre": "Metal/Rap",
        "duration": "5:14", "bpm": 88, "energy": 0.97, "valence": 0.18,
        "emotions": ["angry"], "mood_tags": ["rebellious", "rage", "political"],
        "preview_url": "", "cover": "", "color": "#641E16"
    },
    {
        "id": "a004", "title": "Stronger", "artist": "Kanye West",
        "album": "Graduation", "year": 2007, "genre": "Hip-Hop",
        "duration": "5:11", "bpm": 104, "energy": 0.84, "valence": 0.55,
        "emotions": ["angry", "happy"], "mood_tags": ["powerful", "determined", "confidence"],
        "preview_url": "", "cover": "", "color": "#E74C3C"
    },
    {
        "id": "a005", "title": "In the End", "artist": "Linkin Park",
        "album": "Hybrid Theory", "year": 2000, "genre": "Alternative Metal",
        "duration": "3:36", "bpm": 105, "energy": 0.82, "valence": 0.24,
        "emotions": ["angry", "sad"], "mood_tags": ["frustration", "cathartic", "iconic"],
        "preview_url": "", "cover": "", "color": "#7D3C98"
    },
    {
        "id": "a006", "title": "Seven Nation Army", "artist": "The White Stripes",
        "album": "Elephant", "year": 2003, "genre": "Alternative Rock",
        "duration": "3:51", "bpm": 124, "energy": 0.79, "valence": 0.29,
        "emotions": ["angry"], "mood_tags": ["powerful", "anthemic", "raw"],
        "preview_url": "", "cover": "", "color": "#C0392B"
    },
    {
        "id": "a007", "title": "Lose Yourself", "artist": "Eminem",
        "album": "8 Mile Soundtrack", "year": 2002, "genre": "Hip-Hop",
        "duration": "5:26", "bpm": 171, "energy": 0.92, "valence": 0.29,
        "emotions": ["angry", "happy"], "mood_tags": ["intense", "motivational", "legendary"],
        "preview_url": "", "cover": "", "color": "#D35400"
    },
    {
        "id": "a008", "title": "Bombtrack", "artist": "Rage Against the Machine",
        "album": "Rage Against the Machine", "year": 1992, "genre": "Metal/Rap",
        "duration": "4:03", "bpm": 96, "energy": 0.95, "valence": 0.12,
        "emotions": ["angry"], "mood_tags": ["rebellious", "heavy", "powerful"],
        "preview_url": "", "cover": "", "color": "#922B21"
    },
    {
        "id": "a009", "title": "Run the World (Girls)", "artist": "Beyoncé",
        "album": "4", "year": 2011, "genre": "Pop/Dance",
        "duration": "3:56", "bpm": 125, "energy": 0.93, "valence": 0.63,
        "emotions": ["angry", "happy"], "mood_tags": ["empowering", "fierce", "anthemic"],
        "preview_url": "", "cover": "", "color": "#F39C12"
    },
    {
        "id": "a010", "title": "Numb", "artist": "Linkin Park",
        "album": "Meteora", "year": 2003, "genre": "Alternative Metal",
        "duration": "3:06", "bpm": 110, "energy": 0.74, "valence": 0.20,
        "emotions": ["angry", "sad"], "mood_tags": ["frustration", "emotional", "iconic"],
        "preview_url": "", "cover": "", "color": "#5D6D7E"
    },

    # ═══════════════════════════════════════════
    # CALM / PEACEFUL / NEUTRAL
    # ═══════════════════════════════════════════
    {
        "id": "c001", "title": "Clair de Lune", "artist": "Claude Debussy",
        "album": "Suite bergamasque", "year": 1905, "genre": "Classical",
        "duration": "5:04", "bpm": 60, "energy": 0.09, "valence": 0.49,
        "emotions": ["neutral", "sad"], "mood_tags": ["peaceful", "elegant", "timeless"],
        "preview_url": "", "cover": "", "color": "#85C1E9"
    },
    {
        "id": "c002", "title": "Weightless", "artist": "Marconi Union",
        "album": "Weightless", "year": 2011, "genre": "Ambient",
        "duration": "8:09", "bpm": 60, "energy": 0.06, "valence": 0.32,
        "emotions": ["neutral"], "mood_tags": ["meditative", "anxiety-relief", "sleep"],
        "preview_url": "", "cover": "", "color": "#AED6F1"
    },
    {
        "id": "c003", "title": "Experience", "artist": "Ludovico Einaudi",
        "album": "In a Time Lapse", "year": 2013, "genre": "Neoclassical",
        "duration": "5:13", "bpm": 63, "energy": 0.11, "valence": 0.41,
        "emotions": ["neutral", "sad"], "mood_tags": ["cinematic", "peaceful", "emotional"],
        "preview_url": "", "cover": "", "color": "#D6EAF8"
    },
    {
        "id": "c004", "title": "Gymnopédie No.1", "artist": "Erik Satie",
        "album": "Trois Gymnopédies", "year": 1888, "genre": "Classical",
        "duration": "3:03", "bpm": 56, "energy": 0.05, "valence": 0.37,
        "emotions": ["neutral"], "mood_tags": ["dreamy", "nostalgic", "gentle"],
        "preview_url": "", "cover": "", "color": "#EBF5FB"
    },
    {
        "id": "c005", "title": "Breathe (2 AM)", "artist": "Anna Nalick",
        "album": "Wreck of the Day", "year": 2005, "genre": "Indie Pop",
        "duration": "4:05", "bpm": 94, "energy": 0.30, "valence": 0.38,
        "emotions": ["neutral", "sad"], "mood_tags": ["comforting", "gentle", "introspective"],
        "preview_url": "", "cover": "", "color": "#D5E8D4"
    },
    {
        "id": "c006", "title": "Lo-fi Hip Hop Beats", "artist": "ChillHop Music",
        "album": "Lo-fi Essentials", "year": 2020, "genre": "Lo-fi Hip-Hop",
        "duration": "3:30", "bpm": 75, "energy": 0.38, "valence": 0.55,
        "emotions": ["neutral"], "mood_tags": ["study", "focus", "chill"],
        "preview_url": "", "cover": "", "color": "#FDEBD0"
    },
    {
        "id": "c007", "title": "River", "artist": "Joni Mitchell",
        "album": "Blue", "year": 1971, "genre": "Folk",
        "duration": "4:00", "bpm": 72, "energy": 0.18, "valence": 0.19,
        "emotions": ["neutral", "sad"], "mood_tags": ["introspective", "winter", "regret"],
        "preview_url": "", "cover": "", "color": "#A9CCE3"
    },
    {
        "id": "c008", "title": "Yellow", "artist": "Coldplay",
        "album": "Parachutes", "year": 2000, "genre": "Alternative",
        "duration": "4:29", "bpm": 88, "energy": 0.48, "valence": 0.43,
        "emotions": ["neutral"], "mood_tags": ["gentle", "romantic", "dreamy"],
        "preview_url": "", "cover": "", "color": "#F9E79F"
    },
    {
        "id": "c009", "title": "The Scientist", "artist": "Coldplay",
        "album": "A Rush of Blood to the Head", "year": 2002, "genre": "Alternative",
        "duration": "5:09", "bpm": 76, "energy": 0.32, "valence": 0.23,
        "emotions": ["neutral", "sad"], "mood_tags": ["melancholy", "introspective", "acoustic"],
        "preview_url": "", "cover": "", "color": "#AED6F1"
    },
    {
        "id": "c010", "title": "Mad World", "artist": "Gary Jules",
        "album": "Trading Snakeoil for Wolftickets", "year": 2001, "genre": "Alternative",
        "duration": "3:08", "bpm": 80, "energy": 0.15, "valence": 0.08,
        "emotions": ["neutral", "sad"], "mood_tags": ["somber", "cinematic", "slow"],
        "preview_url": "", "cover": "", "color": "#85929E"
    },

    # ═══════════════════════════════════════════
    # SURPRISE / EXCITED
    # ═══════════════════════════════════════════
    {
        "id": "e001", "title": "Mr. Brightside", "artist": "The Killers",
        "album": "Hot Fuss", "year": 2003, "genre": "Indie Rock",
        "duration": "3:42", "bpm": 148, "energy": 0.93, "valence": 0.41,
        "emotions": ["surprise", "angry"], "mood_tags": ["intense", "anthemic", "indie"],
        "preview_url": "", "cover": "", "color": "#F39C12"
    },
    {
        "id": "e002", "title": "Tití Me Preguntó", "artist": "Bad Bunny",
        "album": "Un Verano Sin Ti", "year": 2022, "genre": "Reggaeton",
        "duration": "4:03", "bpm": 97, "energy": 0.89, "valence": 0.77,
        "emotions": ["surprise", "happy"], "mood_tags": ["party", "energetic", "latin"],
        "preview_url": "", "cover": "", "color": "#F7DC6F"
    },
    {
        "id": "e003", "title": "Dynamite", "artist": "BTS",
        "album": "Dynamite", "year": 2020, "genre": "K-Pop/Disco",
        "duration": "3:19", "bpm": 114, "energy": 0.77, "valence": 0.74,
        "emotions": ["surprise", "happy"], "mood_tags": ["fun", "energetic", "dance"],
        "preview_url": "", "cover": "", "color": "#FF69B4"
    },
    {
        "id": "e004", "title": "Thunderstruck", "artist": "AC/DC",
        "album": "The Razors Edge", "year": 1990, "genre": "Hard Rock",
        "duration": "4:52", "bpm": 134, "energy": 0.97, "valence": 0.62,
        "emotions": ["surprise", "angry"], "mood_tags": ["epic", "powerful", "rock"],
        "preview_url": "", "cover": "", "color": "#E74C3C"
    },
    {
        "id": "e005", "title": "Jump Around", "artist": "House of Pain",
        "album": "House of Pain", "year": 1992, "genre": "Hip-Hop",
        "duration": "3:38", "bpm": 103, "energy": 0.96, "valence": 0.72,
        "emotions": ["surprise", "happy"], "mood_tags": ["hype", "party", "energetic"],
        "preview_url": "", "cover": "", "color": "#D35400"
    },

    # ═══════════════════════════════════════════
    # FEAR / ANXIOUS
    # ═══════════════════════════════════════════
    {
        "id": "f001", "title": "Creep", "artist": "Radiohead",
        "album": "Pablo Honey", "year": 1992, "genre": "Alternative Rock",
        "duration": "3:56", "bpm": 92, "energy": 0.59, "valence": 0.10,
        "emotions": ["fear", "sad"], "mood_tags": ["anxious", "alienation", "raw"],
        "preview_url": "", "cover": "", "color": "#2C3E50"
    },
    {
        "id": "f002", "title": "Under Pressure", "artist": "Queen & David Bowie",
        "album": "Hot Space", "year": 1981, "genre": "Rock",
        "duration": "4:04", "bpm": 110, "energy": 0.77, "valence": 0.44,
        "emotions": ["fear", "neutral"], "mood_tags": ["pressure", "classic", "powerful"],
        "preview_url": "", "cover": "", "color": "#5D6D7E"
    },
    {
        "id": "f003", "title": "Breathin", "artist": "Ariana Grande",
        "album": "Sweetener", "year": 2018, "genre": "Pop",
        "duration": "3:30", "bpm": 99, "energy": 0.56, "valence": 0.35,
        "emotions": ["fear"], "mood_tags": ["anxiety", "overcoming", "empowering"],
        "preview_url": "", "cover": "", "color": "#7FB3D3"
    },
    {
        "id": "f004", "title": "Anxiety", "artist": "Julia Michaels ft. Selena Gomez",
        "album": "Inner Monologue Pt. 1", "year": 2019, "genre": "Pop",
        "duration": "2:57", "bpm": 84, "energy": 0.48, "valence": 0.30,
        "emotions": ["fear"], "mood_tags": ["relatable", "vulnerable", "chill"],
        "preview_url": "", "cover": "", "color": "#85C1E9"
    },
    {
        "id": "f005", "title": "idontwannabeyouanymore", "artist": "Billie Eilish",
        "album": "dont smile at me", "year": 2017, "genre": "Pop",
        "duration": "3:22", "bpm": 96, "energy": 0.22, "valence": 0.14,
        "emotions": ["fear", "sad"], "mood_tags": ["introspective", "vulnerable", "quiet"],
        "preview_url": "", "cover": "", "color": "#283747"
    },

    # ═══════════════════════════════════════════
    # DISGUST / REBELLIOUS
    # ═══════════════════════════════════════════
    {
        "id": "d001", "title": "Smells Like Teen Spirit", "artist": "Nirvana",
        "album": "Nevermind", "year": 1991, "genre": "Grunge",
        "duration": "5:01", "bpm": 117, "energy": 0.92, "valence": 0.35,
        "emotions": ["disgust", "angry"], "mood_tags": ["rebellious", "raw", "iconic"],
        "preview_url": "", "cover": "", "color": "#1C2833"
    },
    {
        "id": "d002", "title": "Basket Case", "artist": "Green Day",
        "album": "Dookie", "year": 1994, "genre": "Punk Rock",
        "duration": "3:01", "bpm": 156, "energy": 0.95, "valence": 0.46,
        "emotions": ["disgust", "angry"], "mood_tags": ["punk", "anxious", "fast"],
        "preview_url": "", "cover": "", "color": "#E74C3C"
    },
    {
        "id": "d003", "title": "Bodies", "artist": "Sex Pistols",
        "album": "Never Mind the Bollocks", "year": 1977, "genre": "Punk",
        "duration": "3:03", "bpm": 150, "energy": 0.97, "valence": 0.22,
        "emotions": ["disgust"], "mood_tags": ["raw", "anarchic", "classic-punk"],
        "preview_url": "", "cover": "", "color": "#922B21"
    },
]


def get_all_songs():
    return SONGS


def get_songs_by_emotion(emotion, limit=20):
    """Return songs matching an emotion, sorted by relevance score"""
    matched = []
    for song in SONGS:
        if emotion in song['emotions']:
            score = 1.0
            if song['emotions'][0] == emotion:
                score = 1.5  # Primary emotion match bonus
            matched.append({**song, 'match_score': score, 'emotion_match': emotion})

    # Sort by match score then by energy relevance
    matched.sort(key=lambda x: x['match_score'], reverse=True)
    return matched[:limit]


def get_songs_by_mood_profile(emotion_scores, limit=15):
    """
    Advanced matching: use full emotion score vector to find best songs.
    Returns songs ranked by weighted cosine similarity.
    """
    emotions_order = ['happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'neutral']
    query_vec = [emotion_scores.get(e, 0) for e in emotions_order]

    scored = []
    for song in SONGS:
        song_vec = []
        for e in emotions_order:
            if e in song['emotions']:
                idx = song['emotions'].index(e)
                weight = 1.0 if idx == 0 else 0.5
                song_vec.append(weight)
            else:
                song_vec.append(0.0)

        # Dot product similarity
        dot = sum(q * s for q, s in zip(query_vec, song_vec))
        q_mag = sum(q**2 for q in query_vec) ** 0.5
        s_mag = sum(s**2 for s in song_vec) ** 0.5

        similarity = dot / (q_mag * s_mag) if (q_mag * s_mag) > 0 else 0
        scored.append({**song, 'match_score': round(similarity, 3), 'emotion_match': 'multi'})

    scored.sort(key=lambda x: x['match_score'], reverse=True)
    return scored[:limit]


def get_song_by_id(song_id):
    for song in SONGS:
        if song['id'] == song_id:
            return song
    return None