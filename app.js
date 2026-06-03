/* Bill Summarizer - frontend logic */

// Tab switching
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
let activeTab = 'text';

tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const tabName = tab.dataset.tab;
    activeTab = tabName;

    tabs.forEach(t => {
      t.classList.toggle('active', t === tab);
      t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
    });

    tabContents.forEach(c => {
      c.classList.toggle('active', c.dataset.content === tabName);
    });
  });
});

// File input display
const fileInput = document.getElementById('bill-file');
const fileName = document.getElementById('file-name');

fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    const file = fileInput.files[0];
    const sizeMB = (file.size / 1024 / 1024).toFixed(1);
    fileName.textContent = `${file.name} (${sizeMB} MB)`;
  } else {
    fileName.textContent = '';
  }
});

// Analyze
const analyzeBtn = document.getElementById('analyze-btn');
const status = document.getElementById('status');
const resultsEl = document.getElementById('results');
const errorEl = document.getElementById('error');

analyzeBtn.addEventListener('click', async () => {
  // Hide previous results/errors
  resultsEl.classList.add('hidden');
  errorEl.classList.add('hidden');

  // Build the form data based on active tab
  const formData = new FormData();

  if (activeTab === 'text') {
    const text = document.getElementById('bill-text').value.trim();
    if (!text) {
      showError('Please paste some bill text.');
      return;
    }
    if (text.length < 200) {
      showError('Text too short. Please paste a substantial portion of a bill (at least a few paragraphs).');
      return;
    }
    formData.append('text', text);
  } else if (activeTab === 'url') {
    const url = document.getElementById('bill-url').value.trim();
    if (!url) {
      showError('Please enter a URL.');
      return;
    }
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      showError('URL must start with http:// or https://');
      return;
    }
    formData.append('url', url);
  } else if (activeTab === 'file') {
    if (fileInput.files.length === 0) {
      showError('Please choose a file to upload.');
      return;
    }
    formData.append('file', fileInput.files[0]);
  }

  // Show loading state
  analyzeBtn.disabled = true;
  status.textContent = 'Analyzing — this can take 30-90 seconds for long bills...';
  status.classList.add('loading');

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    const data = await response.json();
    renderResults(data.analysis, data.source_chars);
  } catch (err) {
    showError(`Analysis failed: ${err.message}`);
  } finally {
    analyzeBtn.disabled = false;
    status.textContent = '';
    status.classList.remove('loading');
  }
});

function showError(message) {
  errorEl.innerHTML = `<strong>Error</strong>${escapeHtml(message)}`;
  errorEl.classList.remove('hidden');
  errorEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function escapeHtml(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderResults(a, sourceChars) {
  let html = '';

  // Title and summary
  html += `<div class="result-block">
    <h2>${escapeHtml(a.title)}</h2>
    <p class="summary-text">${escapeHtml(a.plain_summary)}</p>`;

  // Metadata
  if (a.metadata && Object.keys(a.metadata).length > 0) {
    html += `<div class="metadata-grid">`;
    for (const [key, value] of Object.entries(a.metadata)) {
      const label = key.replace(/_/g, ' ');
      html += `<div class="metadata-item">
        <div class="metadata-label">${escapeHtml(label)}</div>
        <div class="metadata-value">${escapeHtml(value)}</div>
      </div>`;
    }
    html += `<div class="metadata-item">
      <div class="metadata-label">source length</div>
      <div class="metadata-value">${sourceChars.toLocaleString()} chars</div>
    </div>`;
    html += `</div>`;
  }
  html += `</div>`;

  // Sections
  if (a.sections && a.sections.length > 0) {
    html += `<div class="result-block"><h3>Sections</h3>`;
    for (const s of a.sections) {
      const sig = (s.significance || 'medium').toLowerCase();
      html += `<div class="section-item">
        <div class="section-header">
          <span class="section-id">${escapeHtml(s.section_id || '?')}</span>
          <span class="section-heading">${escapeHtml(s.heading || '')}</span>
          <span class="significance-badge sig-${sig}">${escapeHtml(s.significance || 'medium')}</span>
        </div>
        <p class="section-summary">${escapeHtml(s.summary || '')}</p>`;
      if (s.significance_reason) {
        html += `<p class="section-reason">${escapeHtml(s.significance_reason)}</p>`;
      }
      html += `</div>`;
    }
    html += `</div>`;
  }

  // Beneficiaries
  const benef = a.beneficiaries || {};
  const hasBenef = (benef.benefits && benef.benefits.length) ||
                   (benef.costs && benef.costs.length) ||
                   (benef.regulated && benef.regulated.length);
  if (hasBenef) {
    html += `<div class="result-block"><h3>Who's affected</h3><div class="benef-grid">`;
    if (benef.benefits && benef.benefits.length) {
      html += `<div class="benef-column"><h4>Benefits</h4><ul>`;
      for (const item of benef.benefits) {
        html += `<li>${escapeHtml(item)}</li>`;
      }
      html += `</ul></div>`;
    }
    if (benef.costs && benef.costs.length) {
      html += `<div class="benef-column"><h4>Costs / Pays</h4><ul>`;
      for (const item of benef.costs) {
        html += `<li>${escapeHtml(item)}</li>`;
      }
      html += `</ul></div>`;
    }
    if (benef.regulated && benef.regulated.length) {
      html += `<div class="benef-column"><h4>Regulated</h4><ul>`;
      for (const item of benef.regulated) {
        html += `<li>${escapeHtml(item)}</li>`;
      }
      html += `</ul></div>`;
    }
    html += `</div></div>`;
  }

  // Red flags
  if (a.red_flags && a.red_flags.length > 0) {
    html += `<div class="result-block"><h3>Red flags</h3>`;
    // Sort by severity (high first)
    const order = { high: 0, medium: 1, low: 2 };
    const sorted = [...a.red_flags].sort((x, y) =>
      (order[x.severity] ?? 3) - (order[y.severity] ?? 3)
    );
    for (const flag of sorted) {
      const sev = (flag.severity || 'medium').toLowerCase();
      html += `<div class="flag-item severity-${sev}">
        <div class="flag-header">
          <span class="significance-badge sig-${sev}">${escapeHtml(flag.severity || 'medium')}</span>
          <span class="flag-type">${escapeHtml(flag.type || '?')}</span>
          <span class="flag-section">in ${escapeHtml(flag.section || '?')}</span>
        </div>
        <p class="flag-description">${escapeHtml(flag.description || '')}</p>
      </div>`;
    }
    html += `</div>`;
  }

  // Comparable laws
  if (a.comparable_laws && a.comparable_laws.length > 0) {
    html += `<div class="result-block"><h3>Related laws</h3><ul class="simple-list">`;
    for (const law of a.comparable_laws) {
      html += `<li>${escapeHtml(law)}</li>`;
    }
    html += `</ul></div>`;
  }

  // Open questions
  if (a.open_questions && a.open_questions.length > 0) {
    html += `<div class="result-block"><h3>Open questions</h3><ul class="simple-list">`;
    for (const q of a.open_questions) {
      html += `<li>${escapeHtml(q)}</li>`;
    }
    html += `</ul></div>`;
  }

  resultsEl.innerHTML = html;
  resultsEl.classList.remove('hidden');
  resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
