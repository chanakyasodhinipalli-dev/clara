/* ui/static/script.js
   Handles upload, drag-n-drop, AJAX requests to FastAPI, rendering JSON & download links.
   Drop into ui/static/script.js
*/

document.addEventListener('DOMContentLoaded', () => {
  const uploadArea = document.getElementById('uploadArea');
  const fileInput = document.getElementById('fileInput');
  const btnUpload = document.getElementById('btnUpload');
  const previewFrame = document.getElementById('pdfPreview');
  const jsonPane = document.getElementById('jsonPane');
  const downloadsContainer = document.getElementById('downloadsContainer');
  const folderForm = document.getElementById('folderForm');

  // prevent default for drag events
  ['dragenter','dragover','dragleave','drop'].forEach(evt=>{
    uploadArea.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); });
  });

  uploadArea.addEventListener('dragover', () => uploadArea.classList.add('dragover'));
  uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
  uploadArea.addEventListener('drop', (e) => {
    uploadArea.classList.remove('dragover');
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) handleFileSelected(f);
  });

  fileInput.addEventListener('change', (e) => {
    const f = e.target.files && e.target.files[0];
    if (f) handleFileSelected(f);
  });

  btnUpload.addEventListener('click', async (e) => {
    e.preventDefault();
    const f = fileInput.files && fileInput.files[0];
    if (!f) return alert('Please choose a file first.');
    await uploadFile(f);
  });

  folderForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fp = document.getElementById('folderPath').value.trim();
    if (!fp) return alert('Enter folder path');
    await processFolder(fp);
  });

  function handleFileSelected(file){
    // preview PDF if possible
    if (file.type === 'application/pdf') {
      const url = URL.createObjectURL(file);
      previewFrame.setAttribute('src', url);
    } else {
      previewFrame.removeAttribute('src');
    }
    // show filename
    document.getElementById('uploadFilename').innerText = file.name;
  }

  async function uploadFile(file) {
    clearResults();
    setStatus('Uploading & processing...');
    const form = new FormData();
    form.append('file', file);
    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: form
      });
      const data = await res.json();
      if (!res.ok) {
        showError(data.detail || JSON.stringify(data));
        return;
      }
      renderResult(data);
    } catch (err) {
      console.error(err);
      showError('Network error: ' + err.message);
    }
  }

  async function processFolder(folderPath) {
    clearResults();
    setStatus('Processing folder...');
    try {
      const res = await fetch('/api/process-folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder_path: folderPath })
      });
      const data = await res.json();
      if (!res.ok) {
        showError(data.detail || JSON.stringify(data));
        return;
      }
      renderResult(data);
    } catch (err) {
      console.error(err);
      showError('Network error: ' + err.message);
    }
  }

  function renderResult(data) {
    setStatus('Processing complete.');
    jsonPane.textContent = JSON.stringify(data, null, 2);

    // Build downloads list: groups and zip
    downloadsContainer.innerHTML = '';
    if (Array.isArray(data.groups)) {
      data.groups.forEach(g => {
        const el = document.createElement('div');
        el.className = 'download-item';
        const left = document.createElement('div');
        left.className = 'meta';
        const img = document.createElement('img');
        img.src = '/static/pdf_icon.svg';
        img.alt = 'pdf';
        const title = document.createElement('div');
        title.innerHTML = `<div class="title">${g.groupId || 'group'}</div><div class="sub">Pages: ${Array.isArray(g.pageRange)?g.pageRange.join('-'):'-'}</div>`;
        left.appendChild(img);
        left.appendChild(title);

        const right = document.createElement('div');
        right.style.display = 'flex';
        right.style.gap = '8px';

        // Download button
        const dl = document.createElement('a');
        dl.className = 'btn small';
        dl.href = g.downloadUrl || (g.download_url || '#');
        dl.textContent = 'Download';
        dl.target = '_blank';
        dl.rel = 'noopener noreferrer';

        // View JSON button toggles json pane to highlight group
        const viewJson = document.createElement('button');
        viewJson.className = 'btn secondary small';
        viewJson.textContent = 'View JSON';
        viewJson.addEventListener('click', () => {
          // highlight the group's JSON in the JSON pane (very simple)
          const pretty = JSON.stringify(g, null, 2);
          jsonPane.textContent = pretty;
        });

        right.appendChild(viewJson);
        right.appendChild(dl);

        el.appendChild(left);
        el.appendChild(right);
        downloadsContainer.appendChild(el);
      });
    }

    // global ZIP link: API might include zipUrl or zip_path
    if (data.zipUrl || data.zip_path || data.output_zip) {
      const zipLink = (data.zipUrl || data.zip_path || data.output_zip);
      const el = document.createElement('div');
      el.className = 'download-item';
      el.innerHTML = `
        <div class="meta">
          <img src="/static/pdf_icon.svg" alt="zip" />
          <div>
            <div class="title">All Groups (ZIP)</div>
            <div class="sub">Contains group PDFs + metadata</div>
          </div>
        </div>
        <div style="display:flex;gap:8px">
          <a class="btn small" href="${zipLink}" target="_blank" rel="noopener noreferrer">Download ZIP</a>
        </div>
      `;
      downloadsContainer.appendChild(el);
    }
  }

  function setStatus(text){
    const s = document.getElementById('statusText');
    if (s) s.textContent = text;
  }
  function showError(msg){
    setStatus('Error');
    jsonPane.textContent = 'Error: ' + msg;
  }
  function clearResults(){
    jsonPane.textContent = '';
    downloadsContainer.innerHTML = '';
    setStatus('Idle');
  }

  // initial idle
  setStatus('Idle');
});
