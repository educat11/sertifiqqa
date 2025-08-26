/* Client-side certificate generator
   - Parse CSV (Papa Parse), schema-agnostic
   - Show CSV as table
   - Designer: draggable text layers with template content ({{field}})
   - Background image, page size controls
   - Optional QR (base URL + field)
   - Generate PDFs (jsPDF) and ZIP
   - Persist layout to localStorage
*/

(() => {
  const { jsPDF } = window.jspdf;

  const csvInput = document.getElementById('csvInput');
  const bgInput = document.getElementById('bgInput');
  const addCodesBtn = document.getElementById('addCodesBtn');
  const exportCsvBtn = document.getElementById('exportCsvBtn');
  const generateBtn = document.getElementById('generateBtn');
  const statusEl = document.getElementById('status');
  const logEl = document.getElementById('log');
  const pageWEl = document.getElementById('pageW');
  const pageHEl = document.getElementById('pageH');
  const qrBaseEl = document.getElementById('qrBase');
  const qrFieldEl = document.getElementById('qrField');
  const qrEnableEl = document.getElementById('qrEnable');
  const qrXEl = document.getElementById('qrX');
  const qrYEl = document.getElementById('qrY');
  const qrSizeEl = document.getElementById('qrSize');

  const tableEl = document.getElementById('csvTable');
  const previewRowSelect = document.getElementById('previewRowSelect');

  const previewEl = document.getElementById('preview');
  const addTextLayerBtn = document.getElementById('addTextLayerBtn');
  const centerLayerBtn = document.getElementById('centerLayerBtn');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const resetLayoutBtn = document.getElementById('resetLayoutBtn');
  const layersListEl = document.getElementById('layersList');
  const layerEditorEl = document.getElementById('layerEditor');
  const layerTextEl = document.getElementById('layerText');
  const layerSizeEl = document.getElementById('layerSize');
  const layerColorEl = document.getElementById('layerColor');
  const layerXEl = document.getElementById('layerX');
  const layerYEl = document.getElementById('layerY');
  const layerAlignEl = document.getElementById('layerAlign');
  const layerFontEl = document.getElementById('layerFont');
  const layerBoldEl = document.getElementById('layerBold');
  const layerItalicEl = document.getElementById('layerItalic');
  const fontUploadEl = document.getElementById('fontUpload');
  const deleteLayerBtn = document.getElementById('deleteLayerBtn');

  let rows = [];
  let headers = [];
  let bgDataUrl = null;
  let layout = { pageW: 1125, pageH: 870, layers: [] };
  let selectedLayerId = null;
  let previewRowIndex = 0;
  let customFont = null; // { vfsName, family }

  function log(msg) {
    logEl.textContent += msg + "\n";
    logEl.scrollTop = logEl.scrollHeight;
  }

  function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  function saveLayout() {
    try { localStorage.setItem('designerLayout', JSON.stringify(layout)); } catch {}
  }
  function clearLayoutStorage() {
    try { localStorage.removeItem('designerLayout'); } catch {}
  }

  function loadLayout() {
    try {
      const raw = localStorage.getItem('designerLayout');
      if (!raw) return;
      const data = JSON.parse(raw);
      if (typeof data.pageW === 'number') layout.pageW = data.pageW;
      if (typeof data.pageH === 'number') layout.pageH = data.pageH;
      if (Array.isArray(data.layers)) layout.layers = data.layers;
      pageWEl.value = String(layout.pageW);
      pageHEl.value = String(layout.pageH);
    } catch {}
  }

  function setBgPreview() {
    let bg = previewEl.querySelector('.bg');
    if (!bg) { bg = document.createElement('div'); bg.className = 'bg'; previewEl.appendChild(bg); }
    if (bgDataUrl) bg.style.backgroundImage = `url(${bgDataUrl})`; else bg.style.backgroundImage = '';
  }

  function normalizeHeadersFromRows(rs) {
    if (headers && headers.length) return headers;
    if (rs.length === 0) return [];
    const keys = new Set();
    for (const r of rs) Object.keys(r || {}).forEach(k => keys.add(k));
    return Array.from(keys);
  }

  function populatePreviewSelector() {
    if (!previewRowSelect) return;
    previewRowSelect.innerHTML = '';
    const count = rows.length;
    for (let i = 0; i < count; i++) {
      const opt = document.createElement('option');
      opt.value = String(i);
      const label = headers.length ? headers.map(h => rows[i][h]).filter(Boolean).slice(0,2).join(' ') : `Kayıt ${i+1}`;
      opt.textContent = label || `Kayıt ${i+1}`;
      previewRowSelect.appendChild(opt);
    }
    previewRowSelect.value = String(Math.min(previewRowIndex, Math.max(0, count - 1)));
  }

  function renderTable() {
    tableEl.innerHTML = '';
    headers = normalizeHeadersFromRows(rows);
    if (!headers.length) { populatePreviewSelector(); return; }
    const thead = document.createElement('thead');
    const trh = document.createElement('tr');
    headers.forEach(h => { const th = document.createElement('th'); th.textContent = h; trh.appendChild(th); });
    thead.appendChild(trh);
    tableEl.appendChild(thead);

    const tbody = document.createElement('tbody');
    rows.forEach((r, idx) => {
      const tr = document.createElement('tr');
      tr.addEventListener('click', () => { previewRowIndex = idx; if (previewRowSelect) previewRowSelect.value = String(idx); renderPreview(); });
      headers.forEach(h => { const td = document.createElement('td'); td.textContent = r[h] ?? ''; tr.appendChild(td); });
      tbody.appendChild(tr);
    });
    tableEl.appendChild(tbody);
    populatePreviewSelector();
  }

  function compileTemplate(tpl, data) {
    return String(tpl || '').replace(/\{\{\s*([^}]+)\s*\}\}/g, (_m, key) => {
      const k = String(key).trim();
      const v = data && Object.prototype.hasOwnProperty.call(data, k) ? data[k] : '';
      return v == null ? '' : String(v);
    });
  }

  function pxPerPt() {
    const rect = previewEl.getBoundingClientRect();
    const scaleX = rect.width / layout.pageW;
    const scaleY = rect.height / layout.pageH;
    return { sx: scaleX, sy: scaleY };
  }

  function cssAlign(align) {
    if (align === 'center') return 'center';
    if (align === 'right') return 'right';
    return 'left';
  }

  function cssFontFamily(font) {
    if (font === 'times') return 'Times New Roman, Times, serif';
    if (font === 'courier') return 'Courier New, Courier, monospace';
    if (font === 'custom') return 'inherit';
    return 'Helvetica, Arial, sans-serif';
  }

  async function renderPreview() {
    const w = Number(pageWEl.value) || layout.pageW;
    const h = Number(pageHEl.value) || layout.pageH;
    layout.pageW = w; layout.pageH = h; saveLayout();
    previewEl.style.aspectRatio = `${w} / ${h}`;
    setBgPreview();

    Array.from(previewEl.querySelectorAll('.layer, .qr-overlay')).forEach(el => el.remove());

    const row = rows[previewRowIndex] || {};
    const { sx, sy } = pxPerPt();

    layout.layers.forEach(layer => {
      const div = document.createElement('div');
      div.className = 'layer' + (layer.id === selectedLayerId ? ' selected' : '');
      div.dataset.id = layer.id;
      const xpx = (layer.x || 0) * sx;
      const ypx = (layer.y || 0) * sy;
      div.style.left = `${xpx}px`;
      div.style.top = `${ypx}px`;
      div.style.fontSize = `${layer.size || 24}px`;
      div.style.color = layer.color || '#093B6E';
      div.style.fontWeight = layer.bold ? '700' : '400';
      div.style.fontStyle = layer.italic ? 'italic' : 'normal';
      div.style.fontFamily = cssFontFamily(layer.font);
      const align = layer.align || 'left';
      div.style.textAlign = cssAlign(align);
      if (align === 'center') div.style.transform = 'translateX(-50%)';
      else if (align === 'right') div.style.transform = 'translateX(-100%)';
      else div.style.transform = 'none';
      div.textContent = compileTemplate(layer.text, row);
      enableDrag(div, layer);
      div.addEventListener('mousedown', () => selectLayer(layer.id));
      previewEl.appendChild(div);
    });

    // QR overlay in preview
    const includeQr = !!qrEnableEl.checked && !!(qrFieldEl.value || '').trim();
    const code = (qrFieldEl.value || '') && row[qrFieldEl.value] ? row[qrFieldEl.value] : '';
    if (includeQr && code) {
      const base = (qrBaseEl?.value?.trim()) || '';
      const url = joinUrl(base, `${code}.pdf`);
      try {
        const dataUrl = await generateQrDataUrl(url);
        const qx = Number(qrXEl?.value || 0) || 0;
        const qy = Number(qrYEl?.value || 0) || 0;
        const qs = Number(qrSizeEl?.value || 75) || 75;
        const div = document.createElement('div');
        div.className = 'qr-overlay';
        div.style.position = 'absolute';
        div.style.left = `${qx * sx}px`;
        div.style.top = `${qy * sy}px`;
        div.style.width = `${qs * sx}px`;
        div.style.height = `${qs * sy}px`;
        div.style.backgroundImage = `url(${dataUrl})`;
        div.style.backgroundSize = 'cover';
        previewEl.appendChild(div);
      } catch {}
    }
  }

  function enableDrag(el, layer) {
    let dragging = false;
    let startX = 0, startY = 0, startL = 0, startT = 0;

    el.addEventListener('mousedown', (e) => {
      dragging = true;
      const rect = el.getBoundingClientRect();
      startX = e.clientX; startY = e.clientY;
      startL = rect.left; startT = rect.top;
      document.body.style.userSelect = 'none';
    });
    window.addEventListener('mousemove', (e) => {
      if (!dragging) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      const { sx, sy } = pxPerPt();
      const newXPt = Math.max(0, Math.min(layout.pageW, ((startL + dx) - previewEl.getBoundingClientRect().left) / sx));
      const newYPt = Math.max(0, Math.min(layout.pageH, ((startT + dy) - previewEl.getBoundingClientRect().top) / sy));
      layer.x = Math.round(newXPt);
      layer.y = Math.round(newYPt);
      saveLayout();
      renderPreview();
    });
    window.addEventListener('mouseup', () => { dragging = false; document.body.style.userSelect = ''; });
  }

  function selectLayer(id) {
    selectedLayerId = id;
    const layer = layout.layers.find(l => l.id === id);
    if (!layer) { layerEditorEl.classList.add('hidden'); renderPreview(); return; }
    layerEditorEl.classList.remove('hidden');
    layerTextEl.value = layer.text || '';
    layerSizeEl.value = String(layer.size || 24);
    layerColorEl.value = layer.color || '#093B6E';
    layerXEl.value = String(layer.x || 0);
    layerYEl.value = String(layer.y || 0);
    layerAlignEl.value = layer.align || 'left';
    layerFontEl.value = layer.font || 'helvetica';
    layerBoldEl.checked = !!layer.bold;
    layerItalicEl.checked = !!layer.italic;
    renderPreview();
  }

  function addTextLayer() {
    const id = uuidv4();
    const layer = { id, text: '{{ad}} {{soyad}}', size: 30, color: '#093B6E', x: 100, y: 100, align: 'left', font: 'helvetica', bold: false, italic: false };
    layout.layers.push(layer);
    saveLayout();
    renderLayersList();
    selectLayer(id);
  }

  // Reset layout
  if (resetLayoutBtn) resetLayoutBtn.addEventListener('click', () => {
    clearLayoutStorage();
    layout = { pageW: Number(pageWEl.value) || 1125, pageH: Number(pageHEl.value) || 870, layers: [] };
    selectedLayerId = null;
    renderLayersList();
    renderPreview();
    log('Tasarım sıfırlandı.');
  });

  // CSV parsing and wiring
  csvInput.addEventListener('change', async (e) => {
    logEl.textContent = '';
    const file = e.target.files[0];
    if (!file) return;
    statusEl.textContent = 'CSV yükleniyor...';
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (res) => {
        rows = res.data;
        headers = res.meta.fields || normalizeHeadersFromRows(rows);
        statusEl.textContent = `Yüklendi: ${rows.length} kayıt`;
        exportCsvBtn.disabled = false;
        generateBtn.disabled = false;
        addCodesBtn.disabled = false; // optional helper; user can ignore
        renderTable();
        renderPreview();
        log('CSV başarıyla okundu.');
      }
    });
  });

  // hook preview row selector
  if (previewRowSelect) {
    previewRowSelect.addEventListener('change', () => {
      const idx = Number(previewRowSelect.value) || 0;
      previewRowIndex = Math.max(0, Math.min(rows.length - 1, idx));
      renderPreview();
    });
  }
  if (prevBtn) prevBtn.addEventListener('click', () => {
    if (!rows.length) return;
    previewRowIndex = Math.max(0, previewRowIndex - 1);
    if (previewRowSelect) previewRowSelect.value = String(previewRowIndex);
    renderPreview();
  });
  if (nextBtn) nextBtn.addEventListener('click', () => {
    if (!rows.length) return;
    previewRowIndex = Math.min(rows.length - 1, previewRowIndex + 1);
    if (previewRowSelect) previewRowSelect.value = String(previewRowIndex);
    renderPreview();
  });

  // Background handling
  bgInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) { bgDataUrl = null; setBgPreview(); return; }
    statusEl.textContent = 'Arkaplan yükleniyor...';
    bgDataUrl = await fileToDataURL(file);
    statusEl.textContent = 'Arkaplan yüklendi';
    setBgPreview();
  });

  function fileToDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  // Optional: add verification codes into chosen field
  addCodesBtn.addEventListener('click', () => {
    const field = (qrFieldEl.value || 'dogrulama_kodu').trim();
    if (!field) { log('Kod alanı ismi girin.'); return; }
    let added = 0; let caps = 0;
    rows.forEach(r => {
      if (!r[field] || String(r[field]).trim() === '') { r[field] = uuidv4(); added += 1; }
      if (typeof r['ad'] === 'string') { r['ad'] = r['ad'].charAt(0).toUpperCase() + r['ad'].slice(1); caps++; }
      if (typeof r['soyad'] === 'string') { r['soyad'] = r['soyad'].charAt(0).toUpperCase() + r['soyad'].slice(1); caps++; }
    });
    if (!headers.includes(field)) headers.push(field);
    renderTable();
    log(`${added} kod eklendi. Büyük harfe çevrilen alan sayısı: ${caps}`);
  });

  exportCsvBtn.addEventListener('click', () => {
    const csv = Papa.unparse({ fields: headers, data: rows.map(r => headers.map(h => r[h] ?? '')) });
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    saveAs(blob, 'etkinlik_guncel.csv');
  });

  function joinUrl(base, path) {
    if (!base) return path;
    const b = base.endsWith('/') ? base.slice(0, -1) : base;
    const p = path.startsWith('/') ? path : '/' + path;
    return b + p;
  }

  // Designer controls
  addTextLayerBtn.addEventListener('click', addTextLayer);
  if (centerLayerBtn) centerLayerBtn.addEventListener('click', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.align = 'center';
    l.x = Math.round(layout.pageW / 2);
    saveLayout(); renderPreview();
  });

  layerTextEl.addEventListener('input', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.text = layerTextEl.value; saveLayout(); renderPreview();
  });
  layerSizeEl.addEventListener('input', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.size = Number(layerSizeEl.value) || 24; saveLayout(); renderPreview();
  });
  layerColorEl.addEventListener('input', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.color = layerColorEl.value || '#000000'; saveLayout(); renderPreview();
  });
  layerXEl.addEventListener('input', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.x = Number(layerXEl.value) || 0; saveLayout(); renderPreview();
  });
  layerYEl.addEventListener('input', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.y = Number(layerYEl.value) || 0; saveLayout(); renderPreview();
  });
  layerAlignEl.addEventListener('change', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.align = layerAlignEl.value || 'left'; saveLayout(); renderPreview();
  });
  layerFontEl.addEventListener('change', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.font = layerFontEl.value || 'helvetica'; saveLayout(); renderPreview();
  });
  layerBoldEl.addEventListener('change', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.bold = !!layerBoldEl.checked; saveLayout(); renderPreview();
  });
  layerItalicEl.addEventListener('change', () => {
    const l = layout.layers.find(x => x.id === selectedLayerId); if (!l) return;
    l.italic = !!layerItalicEl.checked; saveLayout(); renderPreview();
  });
  if (fontUploadEl) fontUploadEl.addEventListener('change', async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const arrayBuffer = await file.arrayBuffer();
    // convert to base64
    let binary = '';
    const bytes = new Uint8Array(arrayBuffer);
    const chunk = 0x8000;
    for (let i = 0; i < bytes.length; i += chunk) {
      binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
    }
    const base64 = btoa(binary);
    const vfsName = file.name;
    const family = 'custom';
    try {
      jsPDF.API.addFileToVFS(vfsName, base64);
      jsPDF.API.addFont(vfsName, family, 'normal');
      customFont = { vfsName, family };
      const l = layout.layers.find(x => x.id === selectedLayerId); if (l) { l.font = 'custom'; }
      saveLayout(); renderPreview();
      log('Özel font yüklendi.');
    } catch (err) {
      log('Özel font yüklenemedi.');
    }
  });
  deleteLayerBtn.addEventListener('click', () => {
    const idx = layout.layers.findIndex(x => x.id === selectedLayerId);
    if (idx >= 0) layout.layers.splice(idx, 1);
    selectedLayerId = null; saveLayout(); renderLayersList(); renderPreview();
    layerEditorEl.classList.add('hidden');
  });

  pageWEl.addEventListener('input', renderPreview);
  pageHEl.addEventListener('input', renderPreview);

  // PDF generation
  generateBtn.addEventListener('click', async () => {
    const pageW = Number(pageWEl.value) || layout.pageW;
    const pageH = Number(pageHEl.value) || layout.pageH;
    if (!rows.length) { log('Önce CSV yükleyin.'); return; }

    const zip = new JSZip();
    const base = (qrBaseEl?.value?.trim()) || '';
    const qrField = (qrFieldEl?.value?.trim()) || '';
    const includeQr = !!qrEnableEl.checked && !!qrField;
    const qrX = Number(qrXEl?.value || 0) || 0;
    const qrY = Number(qrYEl?.value || 0) || 0;
    const qrSize = Number(qrSizeEl?.value || 75) || 75;

    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      const code = qrField ? (r[qrField] || '') : '';
      const fileName = code ? `${code}.pdf` : `sertifika_${i+1}.pdf`;

      const doc = new jsPDF({ unit: 'pt', format: [pageW, pageH] });
      if (bgDataUrl) {
        try { doc.addImage(bgDataUrl, 'PNG', 0, 0, pageW, pageH, undefined, 'FAST'); }
        catch { try { doc.addImage(bgDataUrl, 'JPEG', 0, 0, pageW, pageH, undefined, 'FAST'); } catch {} }
      }

      if (customFont && customFont.vfsName) {
        try { jsPDF.API.addFont(customFont.vfsName, customFont.family, 'normal'); } catch {}
      }

      layout.layers.forEach(layer => {
        const text = compileTemplate(layer.text, r);
        const family = (layer.font === 'custom' && customFont) ? customFont.family : (layer.font || 'helvetica');
        const style = (layer.bold && layer.italic) ? 'bolditalic' : (layer.bold ? 'bold' : (layer.italic ? 'italic' : 'normal'));
        try { doc.setFont(family, style); } catch {}
        try { doc.setTextColor(layer.color || '#000000'); } catch { doc.setTextColor(0,0,0); }
        doc.setFontSize(Number(layer.size || 24));
        doc.text(String(text || ''), Number(layer.x || 0), Number(layer.y || 0), { align: layer.align || 'left', baseline: 'alphabetic' });
      });

      if (includeQr && code) {
        const url = joinUrl(base, `${code}.pdf`);
        try {
          const qrDataUrl = await generateQrDataUrl(url);
          doc.addImage(qrDataUrl, 'PNG', qrX, qrY, qrSize, qrSize, undefined, 'FAST');
        } catch {}
      }

      const pdfBlob = doc.output('blob');
      zip.file(fileName, pdfBlob);
      log(`${i+1}/${rows.length} → ${fileName} hazır`);
    }

    const zipBlob = await zip.generateAsync({ type: 'blob' });
    saveAs(zipBlob, 'sertifikalar.zip');
    log('ZIP indirildi.');
  });

  async function generateQrDataUrl(text) {
    return new Promise((resolve) => {
      const temp = document.createElement('div');
      temp.style.position = 'fixed';
      temp.style.left = '-9999px';
      document.body.appendChild(temp);
      const qr = new QRCode(temp, { text, width: 300, height: 300, correctLevel: QRCode.CorrectLevel.L });
      setTimeout(() => {
        const img = temp.querySelector('img') || temp.querySelector('canvas');
        const dataUrl = img instanceof HTMLCanvasElement ? img.toDataURL('image/png') : img.src;
        document.body.removeChild(temp);
        resolve(dataUrl);
      }, 50);
    });
  }

  // init
  loadLayout();
  renderLayersList();
  renderPreview();
})();


