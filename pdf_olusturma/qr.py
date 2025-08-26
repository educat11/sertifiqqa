import qrcode
import csv
import os

def qr_olustur():
    # QR kodlarının kaydedileceği klasörün varlığını kontrol et
    klasor_yolu = "qr_foto"
    os.makedirs(klasor_yolu, exist_ok=True)  # Klasör yoksa oluştur

    with open("../liste/etkinlik.csv", encoding="utf-8-sig") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            dogrulama_kodu = satir[5]  # 6. sütun (index 5) doğrulama kodu

            # QR kodu için veriyi belirleyin
            data = f"https://btk-kulup.marmara.edu.tr/dosya/kulup/btk/sertfikalar/{dogrulama_kodu}.pdf"

            # QR kodu oluşturma
            qr = qrcode.QRCode(
                version=3,  # QR kodunun boyutu (1-40 arası)
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Hata düzeltme seviyesi
                box_size=10,  # Her bir kutu boyutunun piksel cinsinden büyüklüğü
                border=1,  # Sınır kalınlığı
            )

            # Veriyi QR koda ekleyin
            qr.add_data(data)
            qr.make(fit=True)

            # Görsel oluşturma
            img = qr.make_image(fill='black', back_color='white')

            # QR kodunu qr_foto klasörüne kaydetme
            dosya_yolu = os.path.join(klasor_yolu, f"{dogrulama_kodu}.png")
            img.save(dosya_yolu)

            print(f"QR kodu kaydedildi: {dosya_yolu}")
