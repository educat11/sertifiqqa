# Sertifika Oluşturucu (GitHub Pages)

Bu klasör, projenin statik web sürümünü içerir. `docs/` klasörü GitHub Pages tarafından otomatik olarak yayınlanabilir.

## Özellikler
- CSV yükle (id, ad, soyad, tarih, eposta, etkinlik [, dogrulama_kodu])
- Eksikse doğrulama kodu (UUID v4) üret
- QR kodu içeren PDF sertifikaları tarayıcıda üret (jsPDF)
- Tüm PDF'leri ZIP olarak indir (JSZip)
- Güncellenmiş CSV'yi indir
- Opsiyonel arkaplan görseli (PNG/JPG)
- QR taban URL'ini yapılandır (ör. `https://kurumunuz.com/sertifikalar/`)

## Dağıtım (GitHub Pages)
1. Bu repoyu GitHub'a gönderin (push).
2. Repo ayarlarında: Settings → Pages → Source: `Deploy from a branch` → Branch: `main` ve Folder: `/docs` olarak seçin.
3. Kaydedin. GitHub Pages, bir kaç dakika içinde `https://<kullanıcı>.github.io/<repo>/` adresinde yayına alır.
4. Sayfayı açtığınızda arayüz yüklenecektir.

## Kullanım
1. CSV dosyasını yükleyin.
2. Gerekliyse "Doğrulama Kodları Ekle" butonuna basın (eksikleri doldurur; `ad/soyad` ilk harflerini büyütür).
3. İsterseniz arkaplan görseli yükleyin ve sayfa boyutlarını ayarlayın.
4. "QR Taban URL" alanına, QR'ın işaret edeceği taban adresi girin (ör. `https://kurumunuz.com/sertifikalar/`).
   - Çıktı linki şu şekilde oluşur: `<QR Taban URL>/<dogrulama_kodu>.pdf` (fazla/eksik `/` otomatik düzeltilir).
5. "PDF Sertifikaları Oluştur (ZIP)" ile indirilebilir ZIP alın.
6. "Güncellenmiş CSV'yi İndir" ile güncel CSV'yi indirin.

## Notlar
- Tüm işlemler istemci tarafında gerçekleşir, sunucu gerektirmez.
- Büyük CSV'lerde tarayıcı belleği sınırlayıcı olabilir.
- Varsayılan QR taban URL: `https://btk-kulup.marmara.edu.tr/dosya/kulup/btk/sertfikalar/`. İhtiyacınıza göre değiştirin.

## Yerel Geliştirme
- Basit bir HTTP sunucu ile test edebilirsiniz:
  - Python 3: `python -m http.server -d docs 8000` ve `http://localhost:8000/` adresine gidin.
- Düzenleyeceğiniz dosyalar:
  - `docs/index.html`: Arayüz ve giriş alanları
  - `docs/styles.css`: Stil
  - `docs/script.js`: İş mantığı (CSV işleme, QR ve PDF üretimi, ZIP)


