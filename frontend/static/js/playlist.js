/**
 * MoodMatch Playlist Page
 * Core Feature: Mood-to-Song Timeline + AI Assistant
 */

const EMOTION_META = {
  happy:    { emoji: '😊', color: '#FFD166', label: 'Happy' },
  sad:      { emoji: '😢', color: '#4A90D9', label: 'Sad' },
  angry:    { emoji: '😠', color: '#FF4F4F', label: 'Angry' },
  surprise: { emoji: '😲', color: '#FF8C42', label: 'Surprised' },
  fear:     { emoji: '😨', color: '#9B59B6', label: 'Fearful' },
  disgust:  { emoji: '🤢', color: '#27AE60', label: 'Disgusted' },
  neutral:  { emoji: '😌', color: '#85C1E9', label: 'Calm' },
};

const GENRE_ICONS = {
  'Pop':'🎤','Rock':'🎸','Hip-Hop':'🎤','Classical':'🎻',
  'Ambient':'🌊','Folk':'🪕','Metal':'🤘','R&B':'🎵','Default':'🎵'
};

// AI responses for common questions
const AI_KNOWLEDGE = {
  "how does this work": "I analyzed your video frame by frame using DeepFace AI. Every second, I detected which emotion was dominant on your face — then matched songs whose energy, tempo, and mood align with what you felt! 🎯",
  "what is the timeline": "The Mood → Song Timeline is the CORE of MoodMatch! It shows exactly which emotion you felt and WHEN — and maps the perfect songs to each emotional moment. For example: 0s→5s you were Happy → Pharrell Williams. 5s→10s you were Sad → Adele. 🎵",
  "how are songs matched": "Songs are matched using a vector similarity algorithm! Each song has scores for energy, valence (positivity), and BPM. Your emotion vector is compared to every song's mood profile using cosine similarity — the closer the match, the higher the % shown! 🎯",
  "what do percentages mean": "The match % tells you how closely a song aligns with your detected emotion. 90%+ = perfect match. 70-89% = great match. Below 70% = general mood match. Higher % = song was specifically chosen for YOUR emotional moment! ✨",
  "can i save playlist": "Right now you can click 📤 Share to copy the playlist link. In the Pro version (coming soon), you'll be able to export directly to Spotify! For now, note down the songs you love by clicking ♥ on them. 💙",
  "what emotions detected": "MoodMatch detects 7 emotions: 😊 Happy, 😢 Sad, 😠 Angry, 😲 Surprised, 😨 Fearful, 🤢 Disgusted, and 😌 Calm/Neutral. The AI analyzes your face every second and picks the strongest emotion in each moment.",
  "upload new video": "Click '↑ New Analysis' in the top navigation to upload a new video! You can record yourself for a few seconds or upload any existing clip. The more expressive your face, the better the results! 🎬",
  "default": "Great question! I'm MoodAI — your emotion music assistant. I analyzed your facial expressions and matched songs to your emotional journey. Ask me anything about your results, how the matching works, or what the timeline means! 🎵"
};

let allSongs = [];
let emotionSummary = {};
let timelineChart = null;
let radarChart = null;

window.addEventListener('DOMContentLoaded', async () => {
  initAIAssistant();
  try {
    await loadResults();
  } catch (err) {
    console.error(err);
    document.getElementById('loadingState').innerHTML =
      `<p style="color:#ff4f4f">Error loading results: ${err.message}</p>`;
  }
});

// ── Load All Data ──────────────────────────────────────────────
async function loadResults() {
  const [recRes, timelineRes] = await Promise.all([
    fetch(`/api/recommendations/${SESSION_ID}`),
    fetch(`/api/emotions/${SESSION_ID}/timeline`)
  ]);

  if (recRes.status === 202) {
    document.getElementById('loadingState').innerHTML =
      `<p style="color:#7C6FFF">Still analyzing... <button onclick="location.reload()" style="color:#7C6FFF;background:none;border:none;cursor:pointer;text-decoration:underline">Refresh</button></p>`;
    setTimeout(() => location.reload(), 3000);
    return;
  }

  if (!recRes.ok) throw new Error('Failed to load recommendations');

  const recData = await recRes.json();
  const timelineData = timelineRes.ok ? await timelineRes.json() : null;

  document.getElementById('loadingState').style.display = 'none';
  document.getElementById('resultsContainer').style.display = 'block';

  emotionSummary = recData.emotion_summary;
  allSongs = recData.recommendations?.songs || [];

  renderEmotionHero(emotionSummary);
  renderRadarChart(emotionSummary.emotion_scores);
  renderEmotionBars(emotionSummary.emotion_scores);

  if (timelineData) {
    renderTimeline(timelineData.timeline);
    renderMoodSongTimeline(timelineData.timeline.segments, allSongs);
  }

  renderPlaylist(recData.recommendations, emotionSummary);
  applyDynamicTheme(emotionSummary.primary_emotion);

  // AI greeting after load
  setTimeout(() => {
    showAIGreeting(emotionSummary);
  }, 1500);
}

// ── Emotion Hero ───────────────────────────────────────────────
function renderEmotionHero(summary) {
  const meta = EMOTION_META[summary.primary_emotion] || EMOTION_META.neutral;
  document.getElementById('emotionEmoji').textContent = meta.emoji;
  document.getElementById('emotionLabel').textContent = meta.label;
  document.getElementById('moodLabel').textContent = summary.mood_label || '';
  document.getElementById('moodMessage').textContent = summary.mood_message || '';
}

// ── Emotion Bars ───────────────────────────────────────────────
function renderEmotionBars(scores) {
  const container = document.getElementById('emotionBars');
  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  container.innerHTML = sorted.map(([emotion, score]) => {
    const meta = EMOTION_META[emotion] || { emoji: '🎵', color: '#7C6FFF', label: emotion };
    const pct = Math.round(score * 100);
    return `
      <div class="emotion-bar-row">
        <div class="emotion-bar-label">${meta.emoji} ${meta.label}</div>
        <div class="emotion-bar-track">
          <div class="emotion-bar-fill" style="width:${pct}%;background:${meta.color}"></div>
        </div>
        <div class="emotion-bar-val">${pct}%</div>
      </div>`;
  }).join('');
}

// ── Radar Chart ────────────────────────────────────────────────
function renderRadarChart(scores) {
  const ctx = document.getElementById('emotionRadar').getContext('2d');
  const emotions = Object.keys(scores);
  const values = emotions.map(e => Math.round(scores[e] * 100));
  const colors = emotions.map(e => EMOTION_META[e]?.color || '#7C6FFF');

  radarChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: emotions.map(e => EMOTION_META[e]?.label || e),
      datasets: [{
        data: values,
        backgroundColor: 'rgba(124,111,255,0.2)',
        borderColor: '#7C6FFF',
        borderWidth: 2,
        pointBackgroundColor: colors,
        pointBorderColor: '#080b14',
        pointRadius: 5,
      }]
    },
    options: {
      responsive: true,
      scales: {
        r: {
          beginAtZero: true, max: 100,
          grid: { color: 'rgba(255,255,255,0.06)' },
          angleLines: { color: 'rgba(255,255,255,0.06)' },
          ticks: { display: false },
          pointLabels: { color: '#8899bb', font: { size: 11, family: 'Inter' } }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
}

// ── Timeline Chart ─────────────────────────────────────────────
function renderTimeline(timeline) {
  if (!timeline?.labels?.length) return;
  const ctx = document.getElementById('timelineChart').getContext('2d');
  const emotions = ['happy', 'sad', 'angry', 'neutral', 'fear', 'surprise'];

  timelineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: timeline.labels,
      datasets: emotions.map(e => ({
        label: EMOTION_META[e]?.label || e,
        data: timeline.datasets[e] || [],
        borderColor: EMOTION_META[e]?.color || '#7C6FFF',
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointRadius: 2,
        tension: 0.4,
      }))
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: '#8899bb', usePointStyle: true, pointStyleWidth: 8 } },
        tooltip: {
          callbacks: {
            title: (items) => {
              const idx = items[0].dataIndex;
              return timeline.range_labels?.[idx]
                ? `⏱ ${timeline.range_labels[idx]}`
                : items[0].label;
            }
          }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#556380', maxTicksLimit: 10 } },
        y: {
          min: 0, max: 1,
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#556380', callback: v => Math.round(v * 100) + '%' }
        }
      }
    }
  });
}

// ══════════════════════════════════════════════════════════════
// CORE FEATURE: MOOD → SONG TIMELINE (Bold + Clear)
// ══════════════════════════════════════════════════════════════
function renderMoodSongTimeline(segments, songs) {
  const container = document.getElementById('moodSongTimeline');
  if (!container || !segments?.length) return;

  // Build emotion → songs map from full song list
  const emotionSongsMap = {};
  songs.forEach(song => {
    (song.emotions || []).forEach(e => {
      if (!emotionSongsMap[e]) emotionSongsMap[e] = [];
      if (emotionSongsMap[e].length < 3) emotionSongsMap[e].push(song);
    });
  });

  container.innerHTML = `
    <!-- Header -->
    <div class="mood-timeline-header">
      <div class="mood-timeline-icon">🎯</div>
      <div>
        <div class="mood-timeline-title">Your Mood → Song Timeline</div>
        <div class="mood-timeline-sub">
          Each moment of your video mapped to the perfect song
        </div>
      </div>
    </div>

    <!-- Segment Cards -->
    ${segments.map((seg, i) => {
      const meta = EMOTION_META[seg.emotion] || { emoji: '😐', color: '#7C6FFF', label: seg.emotion };
      const duration = (seg.end_sec - seg.start_sec).toFixed(1);
      const matchedSongs = emotionSongsMap[seg.emotion] || [];

      // Song rows HTML
      const songsHTML = matchedSongs.length
        ? matchedSongs.map((s, si) => {
            const pct = Math.round((s.match_score || 0) * 100);
            const matchClass = pct >= 80 ? 'seg-match-high' : pct >= 60 ? 'seg-match-mid' : 'seg-match-low';
            const genreIcon = GENRE_ICONS[s.genre?.split('/')[0]] || GENRE_ICONS.Default;
            return `
              <div class="seg-song-row">
                <div class="seg-song-num">${si + 1}</div>
                <div class="seg-song-dot" style="background:${meta.color}22;color:${meta.color}">
                  ${genreIcon}
                </div>
                <div class="seg-song-details">
                  <div class="seg-song-name">${s.title}</div>
                  <div class="seg-song-by">${s.artist} &nbsp;·&nbsp; ${s.genre || ''} &nbsp;·&nbsp; ${s.duration || ''}</div>
                </div>
                <span class="seg-song-genre">${s.genre?.split('/')[0] || ''}</span>
                <span class="seg-match-pct ${matchClass}">${pct}% match</span>
              </div>`;
          }).join('')
        : `<div style="padding:10px 14px;font-size:0.82rem;color:var(--text-3);background:var(--surface);border-radius:8px">
             🎵 General playlist covers this mood
           </div>`;

      return `
        <div class="timeline-segment-card" style="animation-delay:${i * 0.1}s">

          <!-- Top: Emotion + Time Range -->
          <div class="segment-top-bar" style="background:${meta.color}08">
            <div class="segment-number">${i + 1}</div>
            <div class="segment-big-emoji">${meta.emoji}</div>
            <div class="segment-emotion-info">
              <div class="segment-emotion-name" style="color:${meta.color}">
                ${meta.label}
              </div>
            </div>
            <div class="segment-time-badge">
              ⏱&nbsp; ${seg.start_sec}s &nbsp;→&nbsp; ${seg.end_sec}s
            </div>
            <div class="segment-dur-pill">${duration}s</div>
          </div>

          <!-- Bottom: Matched Songs -->
          <div class="segment-songs-area">
            <div class="segment-songs-heading">
              🎧 &nbsp;<span>Songs for this moment</span>
            </div>
            ${songsHTML}
          </div>

        </div>`;
    }).join('')}`;
}

// ── Full Playlist ──────────────────────────────────────────────
function renderPlaylist(recs, summary) {
  const list = document.getElementById('songList');
  document.getElementById('playlistTitle').textContent = recs.playlist_title || 'Full Playlist';
  document.getElementById('playlistDesc').textContent = recs.playlist_description || '';

  const songs = recs.songs || [];
  if (!songs.length) {
    list.innerHTML = '<p style="color:var(--text-2);text-align:center;padding:2rem">No songs found.</p>';
    return;
  }

  list.innerHTML = songs.map((song, i) => {
    const meta = EMOTION_META[song.emotions?.[0]] || { color: '#7C6FFF', emoji: '🎵' };
    const genreEmoji = GENRE_ICONS[song.genre?.split('/')[0]] || GENRE_ICONS.Default;
    const matchPct = Math.round((song.match_score || 0) * 100);
    return `
      <div class="song-card" data-id="${song.id}" style="animation-delay:${i * 0.04}s">
        <div class="song-rank">${song.rank || i + 1}</div>
        <div class="song-color-dot" style="background:${meta.color}22;color:${meta.color}">${genreEmoji}</div>
        <div class="song-info">
          <div class="song-title">${song.title}</div>
          <div class="song-artist">
            ${song.artist}
            <span class="song-reason">${song.recommendation_reason || ''}</span>
          </div>
        </div>
        <div class="song-actions">
          ${matchPct > 0 ? `<span class="match-badge">${matchPct}% match</span>` : ''}
          <span class="song-genre-tag">${song.genre?.split('/')[0] || ''}</span>
          <span class="song-duration">${song.duration || ''}</span>
          <button class="btn-like" data-id="${song.id}">♡</button>
          ${song.preview_url ? `<a class="btn-link" href="${song.preview_url}" target="_blank">↗</a>` : ''}
        </div>
      </div>`;
  }).join('');

  document.querySelectorAll('.btn-like').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const liked = btn.classList.toggle('liked');
      btn.textContent = liked ? '♥' : '♡';
      await fetch('/api/interact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: SESSION_ID, song_id: btn.dataset.id, action: liked ? 'like' : 'play' })
      });
    });
  });
}

// ══════════════════════════════════════════════════════════════
// AI ASSISTANT
// ══════════════════════════════════════════════════════════════
function initAIAssistant() {
  const fab = document.getElementById('aiFab');
  const tooltip = document.getElementById('aiTooltip');
  const sendBtn = document.getElementById('aiSendBtn');
  const input = document.getElementById('aiInput');

  fab?.addEventListener('click', () => {
    tooltip.classList.toggle('open');
  });

  sendBtn?.addEventListener('click', () => handleAIQuery());
  input?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleAIQuery();
  });

  // Suggestion buttons
  document.querySelectorAll('.ai-suggestion-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const q = btn.dataset.q;
      document.getElementById('aiInput').value = q;
      handleAIQuery();
    });
  });
}

function handleAIQuery() {
  const input = document.getElementById('aiInput');
  const responseEl = document.getElementById('aiResponse');
  const query = input.value.trim().toLowerCase();
  if (!query) return;

  // Find best matching response
  let response = AI_KNOWLEDGE['default'];
  for (const [key, val] of Object.entries(AI_KNOWLEDGE)) {
    if (query.includes(key) || key.split(' ').some(w => query.includes(w))) {
      response = val;
      break;
    }
  }

  // Dynamic responses using actual data
  if (query.includes('primary') || query.includes('main') || query.includes('dominant')) {
    const e = emotionSummary.primary_emotion || 'neutral';
    const meta = EMOTION_META[e] || { emoji: '😐', label: e };
    response = `Your primary emotion was ${meta.emoji} ${meta.label}! It appeared most frequently throughout your video. Your mood label is "${emotionSummary.mood_label}" — ${emotionSummary.mood_message || 'a unique emotional fingerprint!'}`;
  }

  if (query.includes('how many song') || query.includes('total song')) {
    response = `I found ${allSongs.length} songs perfectly matched to your emotional profile! Each one was selected based on your specific emotion scores, energy level, and mood intensity. 🎵`;
  }

  responseEl.textContent = response;
  responseEl.style.display = 'block';
  input.value = '';
}

function showAIGreeting(summary) {
  const tooltip = document.getElementById('aiTooltip');
  const msgEl = document.getElementById('aiMessage');
  const e = summary?.primary_emotion || 'neutral';
  const meta = EMOTION_META[e] || { emoji: '😐', label: e };

  if (msgEl) {
    msgEl.textContent = `Hi! I detected you were feeling ${meta.emoji} ${meta.label} (${summary?.mood_label || ''}) — I've mapped your emotions to a personalised playlist. Check the timeline below to see which songs match each moment! Ask me anything 👇`;
  }

  // Auto-open once to show greeting
  if (tooltip) {
    tooltip.classList.add('open');
    setTimeout(() => tooltip.classList.remove('open'), 6000);
  }
}

// ── Theme ──────────────────────────────────────────────────────
function applyDynamicTheme(emotion) {
  const colors = {
    happy:['#FFD166','#FF6B9D'], sad:['#4A90D9','#7C6FFF'],
    angry:['#FF4F4F','#FF8C42'], neutral:['#85C1E9','#7C6FFF'],
    surprise:['#FF8C42','#FFD166'], fear:['#9B59B6','#4A90D9'],
    disgust:['#27AE60','#7C6FFF'],
  };
  const [c1, c2] = colors[emotion] || colors.neutral;
  document.documentElement.style.setProperty('--accent', c1);
  document.documentElement.style.setProperty('--accent-2', c2);
}

// ── Shuffle ────────────────────────────────────────────────────
document.getElementById('shuffleBtn')?.addEventListener('click', () => {
  const list = document.getElementById('songList');
  const cards = [...list.children];
  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    list.appendChild(cards[j]);
  }
  [...list.children].forEach((card, i) => {
    const rank = card.querySelector('.song-rank');
    if (rank) rank.textContent = i + 1;
  });
});

document.getElementById('shareBtn')?.addEventListener('click', () => {
  if (navigator.share) {
    navigator.share({ title: 'MoodMatch Playlist', url: window.location.href });
  } else {
    navigator.clipboard.writeText(window.location.href);
    showToast('Link copied! 📋');
  }
});

function showToast(msg) {
  const t = document.createElement('div');
  t.style.cssText = 'position:fixed;bottom:2rem;right:2rem;background:#7C6FFF22;border:1px solid #7C6FFF66;color:#7C6FFF;padding:.8rem 1.4rem;border-radius:12px;font-size:.85rem;z-index:999;backdrop-filter:blur(10px)';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}