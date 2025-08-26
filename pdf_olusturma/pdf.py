from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
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
resim = "a.jpg"

pdf = canvas.Canvas(dosya_adi)
pdf.setTitle(dosya_basligi)

def kenar_cizgileri(pdf):
    pdf.drawString(100,810,"x100")
    pdf.drawString(200,810,"x200")
    pdf.drawString(300,810,"x300")
    pdf.drawString(400,810,"x400")
    pdf.drawString(500,810,"x500")

    pdf.drawString(10,100,"y100")
    pdf.drawString(10,200,"y200")
    pdf.drawString(10,300,"y300")
    pdf.drawString(10,400,"y400")
    pdf.drawString(10,500,"y500")
    pdf.drawString(10,600,"y600")
    pdf.drawString(10,700,"y700")
    pdf.drawString(10,800,"y800")

kenar_cizgileri(pdf)

pdf.drawInlineImage(resim, 0, 0)

#Kullanılabilir fontlar
for font in pdf.getAvailableFonts():
    print(font)

pdfmetrics.registerFont(
    TTFont("abc", "../DS-DIGI.TTF")
)
pdf.setFont("abc", 36)

# # PDF'ye yazı ekliyoruz
# c.drawString(0, 0, "Merhaba, bu bir PDF dosyasının içeriği!")
# c.drawCentredString(200, 0, "Merhaba, bu bir PDF dosyasının içeriği!")
pdf.drawCentredString(270,770,baslik)

pdf.setFillColorRGB(0, 0, 255)
pdf.setFont("Courier-Bold", 24)
pdf.drawCentredString(290, 720, alt_yazi)

pdf.line(30, 710, 550, 710)

metin = pdf.beginText(40 ,680)
metin.setFont("Courier", 18)
metin.setFillColor(colors.red)

for satir in satirlar:
    metin.textLine(satir)

pdf.drawText(metin)


# PDF dosyasını kaydediyoruz
pdf.save()

print(f"{dosya_adi} başarıyla oluşturuldu!")
