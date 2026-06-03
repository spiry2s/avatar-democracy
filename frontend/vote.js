/* Vote — analyze a bill then have the Avatar vote on it */

const uploadZone = document.getElementById('upload-zone');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const fileName = document.getElementById('file-name');
const textInput = document.getElementById('text-input');
const voteBtn = document.getElementById('vote-btn');
const statusEl = document.getElementById('status');
const statusPrimary = document.getElementById('status-primary');
const statusSecondary = document.getElementById('status-secondary');
const errorEl = document.getElementById('error');
const errorText = document.getElementById('error-text');
const resultsEl = document.getElementById('results');

let activeTab = 'upload';
let selectedFile = null;
let currentVote = null;

// ── Check profile exists ──────────────────────────────────────────────────────

fetch('/api/profile').then(r => r.json()).then(d => {
  if (!d.profile) document.getElementById('no-profile-banner').classList.remove('hidden');
});

// ── Tabs ──────────────────────────────────────────────────────────────────────

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    activeTab = tab.dataset.tab;
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t === tab));
    document.querySelectorAll('.tab-content').forEach(c =>
      c.classList.toggle('active', c.id === `tab-${activeTab}`));
    updateBtn();
  });
});

// ── Upload zone ───────────────────────────────────────────────────────────────

uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault();
  uploadZone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) setFile(fileInput.files[0]); });
document.getElementById('file-clear').addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  fileInfo.classList.add('hidden');
  uploadZone.classList.remove('hidden');
  updateBtn();
});

function setFile(file) {
  if (!file.name.endsWith('.pdf')) { showError('Only PDF upload is supported. Use Paste text otherwise.'); return; }
  selectedFile = file;
  fileName.textContent = `${file.name} (${(file.size / 1048576).toFixed(1)} MB)`;
  fileInfo.classList.remove('hidden');
  uploadZone.classList.add('hidden');
  updateBtn();
}

textInput.addEventListener('input', updateBtn);
function updateBtn() {
  voteBtn.disabled = activeTab === 'upload' ? !selectedFile : textInput.value.trim().length < 100;
}

// ── Analyze then vote ─────────────────────────────────────────────────────────

voteBtn.addEventListener('click', async () => {
  hideError();
  resultsEl.classList.add('hidden');
  setStatus(true, 'Analyzing the bill…', 'Reading and structuring the legislation.');

  try {
    // Step 1: analyze
    const fd = new FormData();
    if (activeTab === 'upload') fd.append('file', selectedFile);
    else fd.append('text', textInput.value.trim());

    const aRes = await fetch('/api/analyze', { method: 'POST', body: fd });
    if (!aRes.ok) throw new Error((await aRes.json()).detail || `Analyze failed (HTTP ${aRes.status})`);
    const analysis = (await aRes.json()).analysis;

    // Step 2: vote
    setStatus(true, 'Your Avatar is voting…', 'Applying your delegates, values, and compass to each section.');
    const vRes = await fetch('/api/avatar/vote', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ analysis }),
    });
    if (!vRes.ok) throw new Error((await vRes.json()).detail || `Vote failed (HTTP ${vRes.status})`);
    currentVote = (await vRes.json()).vote;
    renderVote(currentVote);
  } catch (err) {
    showError(err.message);
  } finally {
    setStatus(false);
  }
});

function setStatus(on, primary, secondary) {
  voteBtn.disabled = on;
  statusEl.classList.toggle('hidden', !on);
  if (on) { statusPrimary.textContent = primary; statusSecondary.textContent = secondary || ''; }
}

// ── Render ────────────────────────────────────────────────────────────────────

function renderVote(vote) {
  document.getElementById('results-title').textContent = `Your Avatar's vote: ${vote.bill_title}`;

  renderTally(vote);
  document.getElementById('recommendation').textContent = vote.recommendation;

  const tensionEl = document.getElementById('tension');
  if (vote.key_tension && vote.key_tension.trim()) {
    tensionEl.innerHTML = `<strong>⚖ Tension in your own configuration:</strong> ${escHtml(vote.key_tension)}`;
    tensionEl.classList.remove('hidden');
  } else {
    tensionEl.classList.add('hidden');
  }

  document.getElementById('sections-count').textContent = vote.section_votes.length;
  const container = document.getElementById('section-votes');
  container.innerHTML = vote.section_votes.map((v, i) => renderSection(v, i)).join('');

  // wire override buttons
  container.querySelectorAll('.override-opt').forEach(btn => {
    btn.addEventListener('click', () => override(parseInt(btn.dataset.idx, 10), btn.dataset.pos));
  });

  resultsEl.classList.remove('hidden');
  resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderTally(vote) {
  const counts = { yes: 0, no: 0, abstain: 0 };
  vote.section_votes.forEach(v => { counts[v.position] = (counts[v.position] || 0) + 1; });
  document.getElementById('tally').innerHTML = `
    <span class="tally-pill tally-yes">${counts.yes} yes</span>
    <span class="tally-pill tally-no">${counts.no} no</span>
    <span class="tally-pill tally-abstain">${counts.abstain} abstain</span>`;
}

function renderSection(v, idx) {
  const pos = (v.position || 'abstain').toLowerCase();
  const basisLabel = formatBasis(v.basis);
  const overridden = v._overridden ? '<span class="sig-badge sig-medium">overridden</span>' : '';
  const diverge = v.divergent ? '<span class="badge-diverge" title="A second model voted differently — treat as low-confidence">⚠ models diverge</span>' : '';
  const drift = v.delegate_drift ? '<span class="badge-drift" title="This vote contradicts the delegate\'s recorded positions — review before trusting it">⚠ delegate drift</span>' : '';
  return `<div class="vote-item vote-${pos}" id="vote-${idx}">
    <div class="vote-header">
      <span class="vote-position pos-${pos}">${escHtml(v.position)}</span>
      <span class="section-id">${escHtml(v.section_id)}</span>
      <span class="section-heading">${escHtml(v.heading)}</span>
      ${overridden}
      ${diverge}
      ${drift}
    </div>
    <p class="vote-reasoning">${escHtml(v.reasoning)}</p>
    <div class="vote-footer">
      <span class="vote-basis">${basisLabel}</span>
      <span class="sig-badge sig-${conf(v.confidence)}">confidence: ${escHtml(v.confidence)}</span>
      <div class="override-group">
        <span class="muted">Override:</span>
        ${['yes', 'no', 'abstain'].map(p =>
          `<button class="override-opt ${pos === p ? 'current' : ''}" data-idx="${idx}" data-pos="${p}">${p}</button>`
        ).join('')}
      </div>
    </div>
  </div>`;
}

function formatBasis(basis) {
  if (!basis) return 'compass';
  if (basis.startsWith('delegate:')) return `following delegate · ${escHtml(basis.slice(9).trim())}`;
  if (basis === 'values') return 'your values statement';
  if (basis === 'compass') return 'your compass (fallback)';
  return escHtml(basis);
}

function conf(c) {
  return c === 'high' ? 'low' : c === 'low' ? 'high' : 'medium'; // green=high confidence, red=low
}

async function override(idx, position) {
  const v = currentVote.section_votes[idx];
  const previous = v.position;
  if (previous === position) return;

  try {
    await fetch('/api/avatar/override', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        bill_title: currentVote.bill_title,
        section_id: v.section_id,
        position,
        previous_position: previous,
      }),
    });
    v.position = position;
    v._overridden = true;
    // re-render this section + tally
    const el = document.getElementById(`vote-${idx}`);
    el.outerHTML = renderSection(v, idx);
    document.getElementById(`vote-${idx}`).querySelectorAll('.override-opt').forEach(btn =>
      btn.addEventListener('click', () => override(parseInt(btn.dataset.idx, 10), btn.dataset.pos)));
    renderTally(currentVote);
  } catch (err) {
    showError(`Override failed: ${err.message}`);
  }
}

// ── Utilities ──────────────────────────────────────────────────────────────────

function showError(msg) { errorText.textContent = msg; errorEl.classList.remove('hidden'); errorEl.scrollIntoView({ behavior: 'smooth' }); }
function hideError() { errorEl.classList.add('hidden'); }
function escHtml(s) {
  if (s == null) return '';
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
