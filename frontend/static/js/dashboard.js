/**
 * MoodMatch Dashboard Analytics Page
 */

window.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/api/analytics');
    const data = await res.json();
    const analytics = data.data;

    document.getElementById('totalSessions').textContent = analytics.total_sessions || 0;

    const topEmotion = analytics.emotion_distribution?.[0];
    document.getElementById('topEmotion').textContent = topEmotion
      ? topEmotion.primary_emotion.charAt(0).toUpperCase() + topEmotion.primary_emotion.slice(1)
      : '—';

    const dist = analytics.emotion_distribution || [];
    if (dist.length) {
      const ctx = document.getElementById('emotionDist').getContext('2d');
      const COLORS = {
        happy: '#FFD166', sad: '#4A90D9', angry: '#FF4F4F',
        neutral: '#85C1E9', surprise: '#FF8C42', fear: '#9B59B6', disgust: '#27AE60'
      };
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: dist.map(d => d.primary_emotion),
          datasets: [{
            data: dist.map(d => d.count),
            backgroundColor: dist.map(d => COLORS[d.primary_emotion] || '#7C6FFF'),
            borderColor: '#0d1220',
            borderWidth: 3,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { labels: { color: '#8899bb', font: { family: 'Inter' } } }
          }
        }
      });
    }
  } catch (err) {
    console.error('Dashboard error:', err);
  }
});