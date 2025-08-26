import csv
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def pdf_oluşturma():

    with open("../liste/etkinlik.csv", encoding="utf-8") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            print(satir)
            dosya_ismi = satir[0] + ".pdf"
            isim_soyisim = satir[1] + " " + satir[2]
            metin = (f'Bilişim Teknolojileri Kulübü (MITC) tarafından\n'
                     f'{satir[3]} tarihinde gerçekleştirilen\n'
                     f'"{satir[4]}" etkinliğine katılımınızdan dolayı\n'
                     f'bu belgeyi almaya hak kazandınız.')
            dogrulama_kodu = satir[5]

            klasor_adi = "sertifikalar"
            if not os.path.exists(klasor_adi):
                os.makedirs(klasor_adi)

            pdf_yolu = os.path.join(klasor_adi, dosya_ismi)

            dosya_basligi = dosya_ismi
            resim = "arkaplan/b.jpg"
            qr_dosya_yolu = f"qr_foto/{dogrulama_kodu}.png"

            pdf = canvas.Canvas(pdf_yolu, pagesize=(1125,870))
            pdf.setTitle(dosya_basligi)

            genislik, yukseklik = pdf._pagesize
            pdf.drawImage(resim,0, 0, width=genislik, height=yukseklik)

            pdfmetrics.registerFont(TTFont("aaa", "arial.ttf"))


            pdf.setFont("aaa", 36)
            pdf.setFillColorRGB(0,0,238)
            pdf.drawCentredString(genislik/2, yukseklik/2, isim_soyisim)

            satirlar = metin.split("\n")
            font_boyutu = 24
            satir_araligi = font_boyutu + 5
            metin_yuksekligi = len(satirlar) * satir_araligi

            metin_baslangic_y = (yukseklik / 2) - 50 - (metin_yuksekligi / 2)
            y_koordinatı = metin_baslangic_y
            pdf.setFont("aaa", font_boyutu)
            for satir in satirlar:
                pdf.drawCentredString(genislik/2, y_koordinatı, satir)
                y_koordinatı -= satir_araligi

            pdf.drawImage(qr_dosya_yolu,1000, 25, width=100, height=100)

            pdf.save()