import csv
import uuid
import qrcode
import os
import shutil
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
import pandas as pd
from pdf2image import convert_from_path


def dogrulama_kodu_olustur_ekle():
    # dogrulama kodu oluşturma
    satirlar = []
    zaten_var = 0
    with open("liste/etkinlik.csv", encoding="utf-8") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            # **Benzersiz doğrulama kodu oluştur**
            doğrulama_kodu = str(uuid.uuid4())  # Benzersiz bir UUID oluştur
            if len(satir) >= 7 and satir[0] != "id":
                zaten_var = 1
            elif satir[0] == "id":
                satirlar.append(satir)
                continue
            else:
                satir[1] = satir[1].capitalize()
                satir[2] = satir[2].capitalize()
                satir.append(doğrulama_kodu)
                satirlar.append(satir)
    if zaten_var == 1:
        print("dogrulama kodu mevcut olduğu için tekrar oluşturulmadı")
    else:
        with open("liste/etkinlik.csv", "w", newline='', encoding="utf-8") as dosya:
            yazilacak = csv.writer(dosya)
            yazilacak.writerows(satirlar)
        print("dogrulama kodu başarıyla eklendi")


def qr_olustur():
    # QR kodlarının kaydedileceği klasörün varlığını kontrol et
    klasor_yolu = "qr_foto"
    os.makedirs(klasor_yolu, exist_ok=True)  # Klasör yoksa oluştur
    basari = 0
    with open("liste/etkinlik.csv", encoding="utf-8-sig") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            if satir[0] != "id":

                dogrulama_kodu = satir[6]  # 6. sütun (index 5) doğrulama kodu

                dosya_yolu = os.path.join(klasor_yolu, f"{dogrulama_kodu}.png")
                if not os.path.exists(dosya_yolu):
                    # QR kodu için veriyi belirleyin
                    data = f"https://btk-kulup.marmara.edu.tr/dosya/kulup/btk/sertfikalar/{dogrulama_kodu}.pdf"

                    # QR kodu oluşturma
                    qr = qrcode.QRCode(
                        version=1,  # QR kodunun boyutu (1-40 arası)
                        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Hata düzeltme seviyesi
                        box_size=10,  # Her bir kutu boyutunun piksel cinsinden büyüklüğü
                        border=0,  # Sınır kalınlığı
                    )

                    # Veriyi QR koda ekleyin
                    qr.add_data(data)
                    qr.make(fit=True)

                    # Görsel oluşturma
                    img = qr.make_image(fill='black', back_color='white')

                    # QR kodunu qr_foto klasörüne kaydetme
                    dosya_yolu = os.path.join(klasor_yolu, f"{dogrulama_kodu}.png")
                    img.save(dosya_yolu)

                    basari = 1
        if basari == 1:
            print("QR kodları başarıyla oluşturuldu.")
        else:
            print("QR kodları mevcut olduğu için oluşturulmadı")


def pdf_olusturma():
    with open("liste/etkinlik.csv", encoding="utf-8") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            print(satir)
            if satir[0] != "id":

                dogrulama_kodu = satir[6]
                isim_soyisim = satir[1] + " " + satir[2]
                dosya_ismi = dogrulama_kodu + ".pdf"
                metin = (f'Bilişim Teknolojileri Kulübü (MITC) tarafından\n'
                         f'{satir[3]} tarihinde gerçekleştirilen\n'
                         f'"{satir[5]}" etkinliğine katılımınızdan dolayı\n'
                         f'bu belgeyi almaya hak kazandınız.')

                klasor_adi = "sertifikalar"
                if not os.path.exists(klasor_adi):
                    os.makedirs(klasor_adi)

                pdf_yolu = os.path.join(klasor_adi, dosya_ismi)

                dosya_basligi = dosya_ismi
                resim = "arkaplan/MITC_Katilim.png"
                qr_dosya_yolu = f"qr_foto/{dogrulama_kodu}.png"

                pdf = canvas.Canvas(pdf_yolu, pagesize=(1125, 870))
                pdf.setTitle(dosya_basligi)

                genislik, yukseklik = pdf._pagesize
                pdf.drawImage(resim, 0, 0, width=genislik, height=yukseklik)

                pdfmetrics.registerFont(TTFont("aaa", "font/Caladea-Regular.ttf"))

                pdf.setFont("aaa", 65)
                pdf.setFillColor("#093B6E")
                pdf.drawCentredString(genislik / 2, (yukseklik / 2) - 25, isim_soyisim)

                satirlar = metin.split("\n")
                font_boyutu = 30
                satir_araligi = font_boyutu + 5
                metin_yuksekligi = len(satirlar) * satir_araligi

                metin_baslangic_y = (yukseklik / 2) - 50 - (metin_yuksekligi / 2)
                y_koordinatı = metin_baslangic_y
                pdf.setFont("aaa", font_boyutu)
                for satir in satirlar:
                    pdf.drawCentredString(genislik / 2, y_koordinatı, satir)
                    y_koordinatı -= satir_araligi

                pdf.drawImage(qr_dosya_yolu, 1010, 37, width=75, height=75)

                pdf.save()
        print("sertfikalar başarıyla oluşturuldu")


def qr_sil():
    klasor_yolu = "qr_foto"
    if not os.path.exists(klasor_yolu):
        print("silinecek klasör bulunamadı")
    else:
        shutil.rmtree(klasor_yolu)
        print("qr klasörü başarıyla silindi")


def pdf_png_donusturme():
    with open("liste/etkinlik.csv") as dosya:
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
                if not os.path.exists("png_donusturme"):
                    os.mkdir("png_donusturme")
                image.save(f'png_donusturme/{dogrulama_kodu}.png', 'PNG')
    print("pdfler png formatına çevrildi")


def tekrar_pdf_olustur():
    with open("liste/etkinlik.csv") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            if satir[0] != "id":
                dogrulama_kodu = satir[6]
                if not os.path.exists("sertfikalar_v2"):
                    os.mkdir("sertfikalar_v2")
                # PDF dosyasının adı ve arka plan resmi
                pdf_filename = f"sertfikalar_v2/{dogrulama_kodu}.pdf"
                background_image = f"png_donusturme/{dogrulama_kodu}.png"

                # PDF dosyasını oluşturuyoruz
                c = canvas.Canvas(pdf_filename, pagesize=(1125, 870))
                # Resmi arka plana yerleştiriyoruz (sayfa boyutuna uyacak şekilde)
                c.drawImage(background_image, 0, 0, width=1125, height=870)

                # PDF dosyasını kaydediyoruz
                c.save()

    print("sertfikalar_v2 oluşturuldu")


def png_sil():
    klasor_yolu = "png_donusturme"
    if not os.path.exists(klasor_yolu):
        print("silinecek klasör yok")
    else:
        shutil.rmtree(klasor_yolu)
        print("png dosyaları silindi")


def mail_gonder_v1():
    # Gmail SMTP sunucu bilgileri
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587  # TLS portu

    # Gönderici bilgileri
    GONDEREN_EMAIL = "nailerkilicoglu6634@gmail.com"
    GONDEREN_SIFRE = "okbj lcyh qndw skzi"
    GONDEREN_ADI = "Bilişim Teknolojileri Kulübü (MITC)"

    # SMTP sunucusuna tek seferde bağlan
    try:
        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.starttls()
        mail.login(GONDEREN_EMAIL, GONDEREN_SIFRE)

        with open("liste/etkinlik.csv", encoding="utf-8") as dosya:
            okundu = csv.reader(dosya)
            for satir in okundu:
                if satir[0] != "id":

                    isim_soyisim = satir[1] + " " + satir[2]
                    mail_adres = satir[4]
                    etkinlik = satir[5]
                    dogrulama_kodu = satir[6]
                    dosya_adi = dogrulama_kodu + ".pdf"
                    pdf_dosyasi = f"sertifikalar/{dosya_adi}"  # Her katılımcının sertifikası

                    # E-posta içeriği
                    mesaj = MIMEMultipart()
                    mesaj["From"] = formataddr((GONDEREN_ADI, GONDEREN_EMAIL))
                    mesaj["To"] = mail_adres
                    mesaj["Subject"] = f"{etkinlik} Etkinliği Katılım Sertifikanız"

                    # E-posta gövdesi
                    govde = f"""Merhaba {isim_soyisim},

        "{etkinlik}" etkinliğimize katılımınız için teşekkür ederiz! Aşağıda, bu etkinliğe gösterdiğiniz ilgi ve katkı için size özel olarak hazırlanmış katılım sertifikanızı bulabilirsiniz.

        Bu sertifika, öğrenmeye ve gelişmeye olan bağlılığınızın bir göstergesi olup, kariyer yolculuğunuzda bir adım daha ileriye taşıyacaktır.

        Gelecek etkinliklerimizde de sizi aramızda görmekten mutluluk duyarız!

        Başarılarınızın devamını dileriz.

        Saygılarımızla,
        Marmara Bilişim Teknolojileri Kulübü
        """
                    mesaj.attach(MIMEText(govde, "plain"))

                    # **📂 PDF ekleme**
                    try:
                        with open(pdf_dosyasi, "rb") as pdf:
                            pdf_icerik = MIMEApplication(pdf.read(), _subtype="pdf")

                            # 📌 **Dosya adı açıkça belirtiliyor**
                            dosya_adi = dogrulama_kodu + ".pdf"
                            pdf_icerik.add_header("Content-Disposition", f'attachment; filename="{dosya_adi}"')

                            mesaj.attach(pdf_icerik)
                    except FileNotFoundError:
                        print(f"HATA: {pdf_dosyasi} bulunamadı, e-posta ek olarak PDF olmadan gönderiliyor.")

                    # E-postayı gönder
                    mail.sendmail(GONDEREN_EMAIL, mail_adres, mesaj.as_string())
                    print(f"{isim_soyisim} için e-posta başarıyla gönderildi!")

        # Bağlantıyı kapat
        mail.quit()
        print("Tüm e-postalar başarıyla gönderildi!")

    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")


def mail_gonder_v2():
    # Gmail SMTP sunucu bilgileri
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587  # TLS portu

    # Gönderici bilgileri
    GONDEREN_EMAIL = "nailerkilicoglu6634@gmail.com"
    GONDEREN_SIFRE = "okbj lcyh qndw skzi"
    GONDEREN_ADI = "Bilişim Teknolojileri Kulübü (MITC)"

    # SMTP sunucusuna tek seferde bağlan
    try:
        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.starttls()
        mail.login(GONDEREN_EMAIL, GONDEREN_SIFRE)

        with open("liste/etkinlik.csv", encoding="utf-8") as dosya:
            okundu = csv.reader(dosya)
            for satir in okundu:
                if satir[0] != "id":

                    isim_soyisim = satir[1] + " " + satir[2]
                    mail_adres = satir[4]
                    etkinlik = satir[5]
                    dogrulama_kodu = satir[6]
                    dosya_adi = dogrulama_kodu + ".pdf"
                    pdf_dosyasi = f"sertifikalar_v2/{dosya_adi}"  # Her katılımcının sertifikası

                    # E-posta içeriği
                    mesaj = MIMEMultipart()
                    mesaj["From"] = formataddr((GONDEREN_ADI, GONDEREN_EMAIL))
                    mesaj["To"] = mail_adres
                    mesaj["Subject"] = f"{etkinlik} Etkinliği Katılım Sertifikanız"

                    # E-posta gövdesi
                    govde = f"""Merhaba {isim_soyisim},

        "{etkinlik}" etkinliğimize katılımınız için teşekkür ederiz! Aşağıda, bu etkinliğe gösterdiğiniz ilgi ve katkı için size özel olarak hazırlanmış katılım sertifikanızı bulabilirsiniz.

        Bu sertifika, öğrenmeye ve gelişmeye olan bağlılığınızın bir göstergesi olup, kariyer yolculuğunuzda bir adım daha ileriye taşıyacaktır.

        Gelecek etkinliklerimizde de sizi aramızda görmekten mutluluk duyarız!

        Başarılarınızın devamını dileriz.

        Saygılarımızla,
        Marmara Bilişim Teknolojileri Kulübü
        """
                    mesaj.attach(MIMEText(govde, "plain"))

                    # **📂 PDF ekleme**
                    try:
                        with open(pdf_dosyasi, "rb") as pdf:
                            pdf_icerik = MIMEApplication(pdf.read(), _subtype="pdf")

                            # 📌 **Dosya adı açıkça belirtiliyor**
                            dosya_adi = dogrulama_kodu + ".pdf"
                            pdf_icerik.add_header("Content-Disposition", f'attachment; filename="{dosya_adi}"')

                            mesaj.attach(pdf_icerik)
                    except FileNotFoundError:
                        print(f"HATA: {pdf_dosyasi} bulunamadı, e-posta ek olarak PDF olmadan gönderiliyor.")

                    # E-postayı gönder
                    mail.sendmail(GONDEREN_EMAIL, mail_adres, mesaj.as_string())
                    print(f"{isim_soyisim} için e-posta başarıyla gönderildi!")

        # Bağlantıyı kapat
        mail.quit()
        print("Tüm e-postalar başarıyla gönderildi!")

    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")


def csv_excel_donustur():
    # CSV dosyasını okuma
    csv_file = 'liste/etkinlik.csv'  # CSV dosyanızın adı ve yolu
    df = pd.read_csv(csv_file)

    # DataFrame'i Excel dosyasına kaydetme
    excel_file = 'liste/etkinlik.xlsx'  # Oluşacak Excel dosyasının adı ve yolu
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"{csv_file} başarıyla {excel_file} dosyasına dönüştürüldü.")

# dogrulama_kodu_olustur_ekle()
# qr_olustur()
# pdf_olusturma()
# qr_sil()
# pdf_png_donusturme()
# tekrar_pdf_olustur()
# png_sil()
# mail_gonder_v1()
# mail_gonder_v2()
# csv_excel_donustur()