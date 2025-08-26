import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

def mail_gonder():

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

        with open("../liste/etkinlik.csv", encoding="utf-8") as dosya:
            okundu = csv.reader(dosya)
            for satir in okundu:
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
