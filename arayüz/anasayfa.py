import sys
import os
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Anasayfa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.klasor_sil()
        self.anasayfa()
    def anasayfa(self):
        self.setWindowTitle("Sertfiqqa Ana Sayfa")
        self.resize(700,600)
        self.setFixedSize(self.size())

        merkez = QWidget(self)
        self.setCentralWidget(merkez)

        layout = QVBoxLayout(merkez)

        self.dosya_yolu = QLabel("Lütfen csv formatında dosya yükleyin",self)
        self.dosya_yolu.setAlignment(Qt.AlignCenter)

        self.dosya_yukle_buton = QPushButton("Dosya Seç",self)
        self.dosya_yukle_buton.clicked.connect(self.dosya_yukle)


        layout.addStretch()
        layout.addWidget(self.dosya_yolu,0,Qt.AlignCenter)
        layout.addWidget(self.dosya_yukle_buton,0,Qt.AlignCenter)
        layout.addStretch()
    def klasor_sil(self):
        if os.path.exists("liste"):
            shutil.rmtree("liste")
    def dosya_yukle(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, 'Dosya Seç', '', 'CSV Dosyaları (*.csv)')

        if dosya_yolu:
            # Dosya yolu etiket üzerinde gösteriliyor
            self.dosya_yolu.setText(f'Seçilen dosya: {dosya_yolu}')

            if not os.path.exists("liste"):
                os.mkdir("liste")
            shutil.copy(dosya_yolu,"liste")
            self.dosya_yukle_buton.hide()

        else:
            self.dosya_yolu.setText(f'Seçilen dosya bulunamadı. Lütfen tekrar deneyin')




if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    pencere = Anasayfa()
    pencere.show()
    sys.exit(uygulama.exec_())
