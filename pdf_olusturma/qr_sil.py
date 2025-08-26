import os
import shutil

def qr_sil():
    klasor_yolu = "qr_foto"
    if not os.path.exists(klasor_yolu):
        print("silinecek klasör bulunamadı")
    else:
        shutil.rmtree(klasor_yolu)
        print("qr klasörü başarıyla silindi")