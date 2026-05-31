/**
 * MoodMatch History Page
 */

const EMOTION_META = {
  happy: { emoji: '😊', label: 'Happy' },
  sad: { emoji: '😢', label: 'Sad' },
  angry: { emoji: '😠', label: 'Angry' },
  surprise: { emoji: '😲', label: 'Surprised' },
  fear: { emoji: '😨', label: 'Fearful' },
  disgust: { emoji: '🤢', label: 'Disgusted' },
  neutral: { emoji: '😌', label: 'Calm' },
};

window.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('historyGrid');

  try {
    const res = await fetch('/api/history');
    const data = await res.json();
    const sessions = data.sessions || [];

    if (!sessions.length) {
      grid.innerHTML = `
        <div style="grid-column:1/-1;text-align:center;padding:4rem;color:var(--text-2)">
          <div style="font-size:3rem;margin-bottom:1rem">🎵</div>
          <p>No analyses yet. <a href="/" style="color:var(--accent)">Upload a video</a> to get started!</p>
        </div>`;
      return;
    }

    grid.innerHTML = sessions.map(session => {
      const emotion = session.primary_emotion || session.emotion_summary?.primary_emotion || 'neutral';
      const meta = EMOTION_META[emotion] || EMOTION_META.neutral;
      const date = new Date(session.created_at).toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
      });
      const status = session.status;
      const isCompleted = status === 'completed';

      return `
        <a href="${isCompleted ? '/playlist/' + session.id : '#'}" 
           class="history-card" 
           style="${!isCompleted ? 'opacity:0.6;cursor:default' : ''}">
          <div class="history-emotion">${meta.emoji}</div>
          <div class="history-title">${session.original_name || 'Unnamed video'}</div>
          <div style="font-size:0.8rem;color:var(--accent);margin-bottom:0.3rem;font-weight:500">
            ${meta.label} ${session.mood_label ? '· ' + session.mood_label : ''}
          </div>
          <div class="history-date">${date}</div>
          <div style="margin-top:0.8rem;display:flex;gap:0.5rem;align-items:center">
            <span style="font-size:0.7rem;padding:3px 10px;border-radius:100px;background:${
              status === 'completed' ? 'rgba(0,212,170,0.15)' :
              status === 'failed' ? 'rgba(255,79,79,0.15)' : 'rgba(124,111,255,0.15)'
            };color:${
              status === 'completed' ? '#00D4AA' :
              status === 'failed' ? '#ff4f4f' : '#7C6FFF'
            }">${status}</span>
            ${session.duration_seconds ? `<span style="font-size:0.75rem;color:var(--text-3)">${Math.round(session.duration_seconds)}s</span>` : ''}
          </div>
        </a>`;
    }).join('');

  } catch (err) {
    grid.innerHTML = `<p style="color:#ff4f4f;text-align:center;padding:2rem">Error: ${err.message}</p>`;
  }
});