/* Minimal client-side flow for GitHub Pages
   - Parse CSV (Papa Parse)
   - Ensure/append verification code (UUID v4)
   - Generate QR (qrcodejs) and PDF (jsPDF) per row
   - Zip PDFs for download (JSZip)
   - Export updated CSV
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

  let rows = [];
  let headers = [];
  let bgDataUrl = null;
  let hasCodes = false;

  function log(msg) {
    logEl.textContent += msg + "\n";
    logEl.scrollTop = logEl.scrollHeight;
  }

  function uuidv4() {
    // RFC4122-ish simple UUID v4
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  function normalizeHeaders(hs) {
    return hs.map(h => (h || '').toString().trim().toLowerCase());
  }

  function ensureColumns() {
    const norm = normalizeHeaders(headers);
    // Required columns
    const required = ['id','ad','soyad','tarih','eposta','etkinlik'];
    for (const col of required) {
      if (!norm.includes(col)) {
        throw new Error(`CSV beklenen sütunu içermiyor: ${col}`);
      }
    }
    // Optional verification code column
    if (!norm.includes('dogrulama_kodu')) {
      headers.push('dogrulama_kodu');
      for (const row of rows) row['dogrulama_kodu'] = '';
      hasCodes = false;
    } else {
      hasCodes = rows.some(r => (r['dogrulama_kodu'] || '').trim().length > 0);
    }
  }

  function fileToDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  function generateQrDataUrl(text) {
    return new Promise((resolve) => {
      const temp = document.createElement('div');
      temp.style.position = 'fixed';
      temp.style.left = '-9999px';
      document.body.appendChild(temp);
      const qr = new QRCode(temp, {
        text,
        width: 300,
        height: 300,
        correctLevel: QRCode.CorrectLevel.L
      });
      setTimeout(() => {
        const img = temp.querySelector('img') || temp.querySelector('canvas');
        const dataUrl = img instanceof HTMLCanvasElement ? img.toDataURL('image/png') : img.src;
        document.body.removeChild(temp);
        resolve(dataUrl);
      }, 50);
    });
  }

  function toCsv(rows, headers) {
    return Papa.unparse({ fields: headers, data: rows.map(r => headers.map(h => r[h] ?? '')) });
  }

  function joinUrl(base, path) {
    if (!base) return path;
    const b = base.endsWith('/') ? base.slice(0, -1) : base;
    const p = path.startsWith('/') ? path : '/' + path;
    return b + p;
  }

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
        headers = res.meta.fields || [];
        try {
          ensureColumns();
          statusEl.textContent = `Yüklendi: ${rows.length} kayıt`;
          addCodesBtn.disabled = false;
          exportCsvBtn.disabled = false;
          generateBtn.disabled = false;
          log('CSV başarıyla okundu.');
        } catch (err) {
          statusEl.textContent = 'CSV hatası';
          log('Hata: ' + err.message);
          addCodesBtn.disabled = true;
          exportCsvBtn.disabled = true;
          generateBtn.disabled = true;
        }
      }
    });
  });

  bgInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) { bgDataUrl = null; return; }
    statusEl.textContent = 'Arkaplan yükleniyor...';
    bgDataUrl = await fileToDataURL(file);
    statusEl.textContent = 'Arkaplan yüklendi';
  });

  addCodesBtn.addEventListener('click', () => {
    let added = 0;
    for (const r of rows) {
      const has = (r['dogrulama_kodu'] || '').trim().length > 0;
      if (!has) {
        r['dogrulama_kodu'] = uuidv4();
        added += 1;
      }
      // Capitalize ad/soyad (ilk harfi büyüt)
      if (typeof r['ad'] === 'string') r['ad'] = r['ad'].charAt(0).toUpperCase() + r['ad'].slice(1);
      if (typeof r['soyad'] === 'string') r['soyad'] = r['soyad'].charAt(0).toUpperCase() + r['soyad'].slice(1);
    }
    hasCodes = rows.some(r => (r['dogrulama_kodu'] || '').trim().length > 0);
    log(`${added} adet doğrulama kodu eklendi.`);
  });

  exportCsvBtn.addEventListener('click', () => {
    const csv = toCsv(rows, headers);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    saveAs(blob, 'etkinlik_guncel.csv');
  });

  generateBtn.addEventListener('click', async () => {
    const pageW = Number(pageWEl.value) || 1125;
    const pageH = Number(pageHEl.value) || 870;
    if (!rows.length) { log('Önce CSV yükleyin.'); return; }
    if (!hasCodes) { log('Önce doğrulama kodlarını ekleyin.'); return; }

    const zip = new JSZip();

    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      if ((r['id'] || '').toLowerCase() === 'id') continue; // başlık satırı varsa
      const name = `${r['ad']} ${r['soyad']}`.trim();
      const etkinlik = r['etkinlik'] || '';
      const tarih = r['tarih'] || '';
      const code = r['dogrulama_kodu'];
      const fileName = `${code}.pdf`;

      const base = qrBaseEl?.value?.trim() || 'https://btk-kulup.marmara.edu.tr/dosya/kulup/btk/sertfikalar/';
      const url = joinUrl(base, `${code}.pdf`);
      const qrDataUrl = await generateQrDataUrl(url);

      const doc = new jsPDF({ unit: 'pt', format: [pageW, pageH] });
      // background
      if (bgDataUrl) {
        try {
          doc.addImage(bgDataUrl, 'PNG', 0, 0, pageW, pageH, undefined, 'FAST');
        } catch {
          // try as JPEG if PNG fails
          try { doc.addImage(bgDataUrl, 'JPEG', 0, 0, pageW, pageH, undefined, 'FAST'); } catch {}
        }
      }

      // name
      doc.setTextColor('#093B6E');
      doc.setFontSize(65);
      doc.text(name, pageW/2, (pageH/2) - 25, { align: 'center' });

      // multi-line message
      const lines = [
        `Bilişim Teknolojileri Kulübü (MITC) tarafından`,
        `${tarih} tarihinde gerçekleştirilen`,
        `"${etkinlik}" etkinliğine katılımınızdan dolayı`,
        `bu belgeyi almaya hak kazandınız.`
      ];
      doc.setTextColor(0,0,0);
      doc.setFontSize(30);
      const lineHeight = 35;
      const startY = (pageH/2) - 50 - (lines.length * lineHeight)/2;
      lines.forEach((ln, idx) => {
        doc.text(ln, pageW/2, startY + idx*lineHeight, { align: 'center' });
      });

      // QR bottom-right (approx to original)
      try {
        doc.addImage(qrDataUrl, 'PNG', pageW - 115, pageH - 115, 75, 75, undefined, 'FAST');
      } catch {}

      const pdfBlob = doc.output('blob');
      zip.file(fileName, pdfBlob);
      log(`${i+1}/${rows.length} → ${fileName} hazır`);
    }

    const zipBlob = await zip.generateAsync({ type: 'blob' });
    saveAs(zipBlob, 'sertifikalar.zip');
    log('ZIP indirildi.');
  });
})();


