from pdf2image import convert_from_path
import csv

def pdf_png_donusturme():
    with open("etkinlik.csv") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            if satir[0] != "id":
                dogrulama_kodu = satir[6]

                # PDF dosyasının yolu
                pdf_path = f'sertifikalar/{dogrulama_kodu}.pdf'

                # Poppler'ın bin klasörünün tam yolunu belirtin
                poppler_path = r'C:\Users\Acer\Desktop\sertfika\.venv\Lib\site-packages\poppler-24.08.0\Library\bin'

                # PDF'yi sayfalara ayırarak PNG'ye dönüştürme
                pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)

                # İlk sayfayı al
                image = pages[0]

                image.save(f'png_donusturme/{dogrulama_kodu}.png', 'PNG')