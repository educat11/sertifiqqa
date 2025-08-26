import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from anasayfa import Anasayfa

class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.giris()

    def giris(self):
        self.setWindowTitle("Sertfiqqa")
        self.resize(700, 600)
        self.setFixedSize(self.size())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.baslik = QLabel("Sertfiqqaya Hoşgeldiniz", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        self.giris_buton = QPushButton("Giriş Yap", self)
        self.giris_buton.clicked.connect(self.giris_yap)

        self.kayit_buton = QPushButton("Kayıt Ol", self)
        self.kayit_buton.clicked.connect(self.kayit_ol)

        self.hakkimizda_buton = QPushButton("Hakkımızda", self)
        self.hakkimizda_buton.clicked.connect(self.hakkimizda)

        layout.addStretch()
        layout.addWidget(self.baslik, 0, Qt.AlignCenter)
        layout.addWidget(self.giris_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.kayit_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.hakkimizda_buton, 0, Qt.AlignCenter)
        layout.addStretch()

    def giris_yap(self):
        self.close()
        self.giris_yap = Giris_sayfasi()
        self.giris_yap.show()

    def kayit_ol(self):
        pass

    def hakkimizda(self):
        pass

class Giris_sayfasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.giris_sayfasi()
    def giris_sayfasi(self):
        self.setWindowTitle("Sertfiqqa")
        self.resize(700,600)
        self.setFixedSize(self.size())

        merkez = QWidget(self)
        self.setCentralWidget(merkez)

        layout = QVBoxLayout(merkez)

        self.baslik = QLabel("Giriş Yap", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        self.kullanici = QLineEdit(self)
        self.kullanici.setPlaceholderText("Kullanıcı adı")

        self.sifre = QLineEdit(self)
        self.sifre.setPlaceholderText("Şifre")

        self.giris_buton = QPushButton("Giriş Yap", self)
        self.giris_buton.clicked.connect(self.giris_yap)

        self.geridon_buton = QPushButton("Geri Dön", self)
        self.geridon_buton.clicked.connect(self.geri_don)

        layout.addStretch()
        layout.addWidget(self.baslik, 0, Qt.AlignCenter)
        layout.addWidget(self.kullanici, 0, Qt.AlignCenter)
        layout.addWidget(self.sifre, 0, Qt.AlignCenter)
        layout.addWidget(self.giris_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.geridon_buton, 0, Qt.AlignCenter)
        layout.addStretch()

    def giris_yap(self):
        self.close()
        self.anasayfa = Anasayfa()
        self.anasayfa.show()
    def geri_don(self):
        self.close()
        self.giris_ekrani = GirisEkrani()
        self.giris_ekrani.show()



if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    pencere = GirisEkrani()
    pencere.show()
    sys.exit(uygulama.exec_())
