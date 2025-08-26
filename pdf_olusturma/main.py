from reportlab.pdfgen import canvas
from reportlab.lib import colors

dosya_adi = "dosya_adi.pdf"
dosya_basligi = "dosya_basligi"
baslik = "baslik"
alt_yazi = "alt_yazi"
satirlar = [
    "1.satir metin",
    "2.satir metin",
    "3.satir metin"
]
resim = "a.jpg"  # Arka plan resmi

# 2344x1811 piksel boyutunda bir PDF oluşturuluyor
pdf = canvas.Canvas(dosya_adi, pagesize=(1125, 870))  # 1125x870 yerine uygun boyut kullanın
pdf.setTitle(dosya_basligi)

# Sayfa boyutunu alıyoruz (width, height)
width, height = pdf._pagesize

# Arka plan resmini sayfaya sığacak şekilde ekliyoruz
pdf.drawImage(resim, 0, 0, width=width, height=height)

# Başlık
pdf.setFont("Helvetica-Bold", 36)  # Büyük font kullanılıyor
pdf.setFillColor(colors.black)  # Siyah renk
pdf.drawCentredString(width / 2, height - 80, baslik)

# Alt yazı
pdf.setFont("Helvetica", 24)  # Alt yazı için farklı bir font
pdf.setFillColorRGB(0, 0, 255)  # Mavi renk
pdf.drawCentredString(width / 2, height - 130, alt_yazi)

# Yatay çizgi
pdf.line(30, height - 140, width - 30, height - 140)

# Satırlar için metin
metin = pdf.beginText(40, height - 180)
metin.setFont("Helvetica", 18)
metin.setFillColor(colors.red)

for satir in satirlar:
    metin.textLine(satir)

pdf.drawText(metin)

# PDF dosyasını kaydediyoruz
pdf.save()

print(f"{dosya_adi} başarıyla oluşturuldu!")
