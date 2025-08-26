import PyPDF2

# PDF dosyasının yolunu belirleyin
pdf_dosyasi = 'jQUsp4CW3R.pdf'

# PDF dosyasını açıyoruz
with open(pdf_dosyasi, 'rb') as dosya:
    pdf_reader = PyPDF2.PdfReader(dosya)

    # İlk sayfanın boyutlarını alıyoruz
    sayfa = pdf_reader.pages[0]

    # Sayfa boyutları: (sol, üst, sağ, alt) koordinatları
    boyut = sayfa.mediabox

    # Sayfa genişliği ve yüksekliği
    print(f"Sayfa Genişliği: {boyut.width}")
    print(f"Sayfa Yüksekliği: {boyut.height}")
