import csv
import uuid

def dogrulama_kodu_olustur():
    # dogrulama kodu oluşturma
    satirlar = []
    with open("../liste/etkinlik.csv", encoding="utf-8") as dosya:
        okundu = csv.reader(dosya)
        for satir in okundu:
            # **Benzersiz doğrulama kodu oluştur**
            doğrulama_kodu = str(uuid.uuid4())  # Benzersiz bir UUID oluştur
            satir.append(doğrulama_kodu)
            satirlar.append(satir)
    with open("../liste/etkinlik.csv", "w", newline='', encoding="utf-8") as dosya:
            yazilacak = csv.writer(dosya)
            yazilacak.writerows(satirlar)