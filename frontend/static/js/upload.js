/**
 * MoodMatch Upload Page JavaScript
 * Handles: drag & drop, file selection, upload, status polling
 */

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const uploadCard = document.getElementById('uploadCard');
const processingOverlay = document.getElementById('processingOverlay');

let selectedFile = null;
let pollingInterval = null;

// ─── Drag & Drop ──────────────────────────────────────────────
['dragenter', 'dragover'].forEach(evt => {
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });
});

['dragleave', 'drop'].forEach(evt => {
  dropZone.addEventListener(evt, () => {
    dropZone.classList.remove('drag-over');
  });
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file && isValidVideo(file)) {
    handleFileSelected(file);
  } else {
    showError('Please drop a valid video file (MP4, MOV, AVI, MKV, WEBM)');
  }
});

dropZone.addEventListener('click', (e) => {
  if (e.target.tagName !== 'BUTTON') {
    fileInput.click();
  }
});

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) {
    handleFileSelected(fileInput.files[0]);
  }
});

// ─── File Handling ─────────────────────────────────────────────
function isValidVideo(file) {
  const validTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska', 'video/webm', 'video/x-msvideo'];
  const validExts = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'];
  const ext = file.name.split('.').pop().toLowerCase();
  return validTypes.includes(file.type) || validExts.includes(ext);
}

function handleFileSelected(file) {
  selectedFile = file;

  // Show preview
  document.getElementById('fileName').textContent = file.name;
  document.getElementById('fileSize').textContent = formatBytes(file.size);

  // Show video thumbnail
  const videoEl = document.getElementById('videoPreview');
  videoEl.src = URL.createObjectURL(file);

  // Switch to preview state
  dropZone.style.display = 'none';
  filePreview.style.display = 'block';
}

document.getElementById('removeFile').addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  dropZone.style.display = 'block';
  filePreview.style.display = 'none';
  document.getElementById('videoPreview').src = '';
});

// ─── Upload & Process ──────────────────────────────────────────
document.getElementById('analyzeBtn').addEventListener('click', startAnalysis);

async function startAnalysis() {
  if (!selectedFile) return;

  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true;
  btn.querySelector('.btn-text').textContent = 'Uploading...';

  showProcessingOverlay();

  const formData = new FormData();
  formData.append('video', selectedFile);

  try {
    setStep(1, 'active');
    updateProgress(10, 'Uploading your video...');

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Upload failed');
    }

    setStep(1, 'done');
    setStep(2, 'active');
    updateProgress(30, 'Detecting faces in your video...');

    // Start polling
    pollStatus(data.session_id);

  } catch (err) {
    hideProcessingOverlay();
    btn.disabled = false;
    btn.querySelector('.btn-text').textContent = 'Analyze My Mood';
    showError('Upload failed: ' + err.message);
  }
}

function pollStatus(sessionId) {
  let attempts = 0;
  const maxAttempts = 180;  // 180 × 5sec = 15 min max wait

  pollingInterval = setInterval(async () => {
    attempts++;
    if (attempts > maxAttempts) {
      clearInterval(pollingInterval);
      hideProcessingOverlay();
      showError('Analysis is taking too long. Please try again.');
      return;
    }

    try {
      const res = await fetch(`/api/status/${sessionId}`);
      const data = await res.json();

      updateStatusUI(data.status, attempts);

      if (data.status === 'completed') {
        clearInterval(pollingInterval);
        setStep(4, 'done');
        updateProgress(100, 'Your playlist is ready! 🎵');

        setTimeout(() => {
          window.location.href = `/playlist/${sessionId}`;
        }, 800);
      } else if (data.status === 'failed') {
        clearInterval(pollingInterval);
        hideProcessingOverlay();
        showError('Analysis failed: ' + (data.error || 'Unknown error'));
      }
    } catch (err) {
      console.error('Polling error:', err);
    }
  }, 5000);  // poll every 5 seconds
}

function updateStatusUI(status, attempts) {
  const progress = {
    'processing': 20,
    'analyzing': 50,
    'completed': 100,
  };

  const messages = {
    'processing': { title: 'Processing video...', sub: 'Preparing frames for analysis' },
    'analyzing': { title: 'Detecting emotions...', sub: 'AI is reading your facial expressions' },
  };

  const msg = messages[status] || { title: 'Matching your music...', sub: 'Almost there!' };
  const p = progress[status] || Math.min(20 + attempts * 0.5, 90);  // slower progress increment

  updateProgress(p, msg.title);
  document.getElementById('processingTitle').textContent = msg.title;
  document.getElementById('processingSub').textContent = msg.sub;

  // Update steps
  if (status === 'analyzing') {
    setStep(2, 'done');
    setStep(3, 'active');
  }
  if (p > 70) {
    setStep(3, 'done');
    setStep(4, 'active');
  }
}

// ─── UI Helpers ────────────────────────────────────────────────
function showProcessingOverlay() {
  processingOverlay.style.display = 'flex';
  updateProgress(5, 'Starting upload...');
}

function hideProcessingOverlay() {
  processingOverlay.style.display = 'none';
  document.getElementById('analyzeBtn').disabled = false;
  document.getElementById('analyzeBtn').querySelector('.btn-text').textContent = 'Analyze My Mood';
}

function updateProgress(pct, title) {
  document.getElementById('progressFill').style.width = pct + '%';
  if (title) document.getElementById('processingTitle').textContent = title;
}

function setStep(num, state) {
  const el = document.getElementById(`step${num}`);
  if (!el) return;
  el.className = 'step ' + state;
  if (state === 'done') {
    el.querySelector('.step-dot').textContent = '';
  }
}

function showError(msg) {
  const existing = document.querySelector('.error-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'error-toast';
  toast.style.cssText = `
    position: fixed; bottom: 2rem; right: 2rem; z-index: 999;
    background: #ff4f4f22; border: 1px solid #ff4f4f66; color: #ff8888;
    padding: 1rem 1.5rem; border-radius: 12px; font-size: 0.9rem;
    max-width: 400px; backdrop-filter: blur(10px);
  `;
  toast.textContent = '⚠️ ' + msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 5000);
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}
