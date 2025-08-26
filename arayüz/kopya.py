import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime


def veritabani():
    global baglanti
    global imlec

    baglanti = sqlite3.connect('../liste.db')
    imlec = baglanti.cursor()
    imlec.execute('''
        CREATE TABLE IF NOT EXISTS kisiler (
        tc INT NOT NULL,
        ad VARCHAR(45) NOT NULL,
        soyad VARCHAR(45) NOT NULL,
        dogum_tarihi DATE NOT NULL,
        burc VARCHAR(45) NOT NULL,
        PRIMARY KEY(tc)
        );
    ''')
    baglanti.commit()


def burc_bul(gun, ay):
    if ay == 1:
        if gun <= 20:
            return "Oğlak"
        else:
            return "Kova"
    elif ay == 2:
        if gun <= 19:
            return "Kova"
        else:
            return "Balık"
    elif ay == 3:
        if gun <= 20:
            return "Balık"
        else:
            return "Koç"
    elif ay == 4:
        if gun <= 20:
            return "Koç"
        else:
            return "Boğa"
    elif ay == 5:
        if gun <= 20:
            return "Boğa"
        else:
            return "İkizler"
    elif ay == 6:
        if gun <= 21:
            return "İkizler"
        else:
            return "Yengeç"
    elif ay == 7:
        if gun <= 22:
            return "Yengeç"
        else:
            return "Aslan"
    elif ay == 8:
        if gun <= 23:
            return "Aslan"
        else:
            return "Başak"
    elif ay == 9:
        if gun <= 23:
            return "Başak"
        else:
            return "Terazi"
    elif ay == 10:
        if gun <= 23:
            return "Terazi"
        else:
            return "Akrep"
    elif ay == 11:
        if gun <= 22:
            return "Akrep"
        else:
            return "Yay"
    elif ay == 12:
        if gun <= 21:
            return "Yay"
        else:
            return "Oğlak"


class GirisEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.giris()

    def giris(self):
        self.setWindowTitle("Doğum Günü Hatırlatıcı")
        self.resize(700, 600)
        self.setFixedSize(self.size())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.baslik = QLabel("Doğum Günü Hatırlatıcı", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        self.kayit_ekle_sil_buton = QPushButton("Kişi Ekle/Sil", self)
        self.kayit_ekle_sil_buton.clicked.connect(self.kisi_ekleme_silme)

        self.listele_buton = QPushButton("Kişileri Listele", self)
        self.listele_buton.clicked.connect(self.listele)

        layout.addStretch()
        layout.addWidget(self.baslik, 0, Qt.AlignCenter)
        layout.addWidget(self.kayit_ekle_sil_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.listele_buton, 0, Qt.AlignCenter)
        layout.addStretch()

    def kisi_ekleme_silme(self):
        self.close()
        self.ekle_sil = Ekleme()
        self.ekle_sil.show()

    def listele(self):
        self.close()
        self.listeleme = Listeleme()
        self.listeleme.show()


class Ekleme(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ekle_arayuz()

    def ekle_arayuz(self):
        self.setWindowTitle("Doğum Günü Hatırlatıcı")
        self.resize(700, 600)
        self.setFixedSize(self.size())

        merkez = QWidget(self)
        self.setCentralWidget(merkez)

        layout = QVBoxLayout(merkez)

        self.baslik = QLabel("Kişi Ekle/Sil", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        self.tc = QLineEdit(self)
        self.tc.setPlaceholderText("TC")

        self.ad = QLineEdit(self)
        self.ad.setPlaceholderText("Ad")

        self.soyad = QLineEdit(self)
        self.soyad.setPlaceholderText("Soyad")

        self.dogum = QDateEdit(self)
        self.dogum.setCalendarPopup(True)
        self.dogum.setDisplayFormat("dd-MM-yyyy")

        self.ekle_buton = QPushButton("Kişiyi Ekle", self)
        self.ekle_buton.clicked.connect(self.eklemeye_basildi)

        self.geridon_buton = QPushButton("Geri Dön", self)
        self.geridon_buton.clicked.connect(self.geridone_basildi)

        layout.addStretch()
        layout.addWidget(self.baslik, 0, Qt.AlignCenter)
        layout.addWidget(self.tc, 0, Qt.AlignCenter)
        layout.addWidget(self.ad, 0, Qt.AlignCenter)
        layout.addWidget(self.soyad, 0, Qt.AlignCenter)
        layout.addWidget(self.dogum, 0, Qt.AlignCenter)
        layout.addWidget(self.ekle_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.geridon_buton, 0, Qt.AlignCenter)
        layout.addStretch()

    def eklemeye_basildi(self):
        veritabani()

        try:
            tc = int(self.tc.text())
            ad = self.ad.text()
            soyad = self.soyad.text()
            dogum_tarihi = self.dogum.date().toString("yyyy-MM-dd")
            gun = self.dogum.date().day()
            ay = self.dogum.date().month()
            burc = burc_bul(gun, ay)

            imlec.execute('''
                INSERT INTO kisiler(tc, ad, soyad, dogum_tarihi, burc)
                VALUES(?, ?, ?, ?, ?)''', (tc, ad, soyad, dogum_tarihi, burc))
            baglanti.commit()
            QMessageBox.information(self, 'Başarılı', 'Kişi başarıyla eklendi!')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', str(e))
        finally:
            baglanti.close()

    def geridone_basildi(self):
        self.close()
        self.giris_ekrani = GirisEkrani()
        self.giris_ekrani.show()


class Listeleme(QMainWindow):
    def __init__(self):
        super().__init__()
        self.listele_arayuz()

    def listele_arayuz(self):
        self.setWindowTitle("Doğum Günü Hatırlatıcı")
        self.resize(700, 600)
        self.setFixedSize(self.size())

        merkez = QWidget(self)
        self.setCentralWidget(merkez)

        layout = QVBoxLayout(merkez)

        self.baslik = QLabel("Kişileri Listele", self)
        self.baslik.setAlignment(Qt.AlignCenter)

        self.listele_buton = QPushButton("Kişileri Listele", self)
        self.listele_buton.clicked.connect(self.listelemeye_basildi)

        self.sirala_buton = QPushButton("Tarihe Göre Sırala", self)
        self.sirala_buton.clicked.connect(self.sirala)

        self.geridon_buton = QPushButton("Geri Dön", self)
        self.geridon_buton.clicked.connect(self.geridone_basildi)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(['TC', 'Ad', 'Soyad', 'Doğum Tarihi', 'Burç'])

        layout.addStretch()
        layout.addWidget(self.baslik, 0, Qt.AlignCenter)
        layout.addWidget(self.listele_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.sirala_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.geridon_buton, 0, Qt.AlignCenter)
        layout.addWidget(self.tablo)
        layout.addStretch()

    def listelemeye_basildi(self):
        veritabani()
        imlec.execute("SELECT * FROM kisiler")
        liste = imlec.fetchall()
        baglanti.close()

        if not liste:
            QMessageBox.warning(self, 'Uyarı', 'Listelenecek kayıt bulunamadı!')
            return
        else:
            QMessageBox.information(self, 'Başarılı', 'Kişiler başarıyla listelendi!')

        self.tablo.setRowCount(len(liste))
        for i, kisi in enumerate(liste):
            for j, bilgi in enumerate(kisi):
                self.tablo.setItem(i, j, QTableWidgetItem(str(bilgi)))

    def sirala(self):
        veritabani()
        imlec.execute("SELECT * FROM kisiler")
        liste = imlec.fetchall()
        baglanti.close()

        if not liste:
            QMessageBox.warning(self, 'Uyarı', 'Listelenecek kayıt bulunamadı!')
            return

        # Bugünün tarihini al
        bugun = datetime.today()
        yil = bugun.year

        # Doğum günlerini günümüze en yakın tarihe göre sıralamak için güncel tarihleri hesapla
        kisiler_guncel = []
        for kisi in liste:
            tc, ad, soyad, dogum_tarihi, burc = kisi
            dogum = datetime.strptime(dogum_tarihi, '%Y-%m-%d')
            guncel_dogum_tarihi = dogum.replace(year=yil)

            # Eğer güncel doğum tarihi bugünden önce ise bir sonraki yıla al
            if guncel_dogum_tarihi < bugun:
                guncel_dogum_tarihi = guncel_dogum_tarihi.replace(year=yil + 1)

            kisiler_guncel.append((tc, ad, soyad, dogum_tarihi, burc, guncel_dogum_tarihi))

        # Güncel doğum tarihine göre sırala
        kisiler_guncel.sort(key=lambda x: x[5])

        # Tabloyu güncelle
        self.tablo.setRowCount(len(kisiler_guncel))
        for i, kisi in enumerate(kisiler_guncel):
            for j, bilgi in enumerate(kisi[:5]):
                self.tablo.setItem(i, j, QTableWidgetItem(str(bilgi)))

        QMessageBox.information(self, 'Başarılı', 'Kişiler başarıyla sıralandı!')

    def geridone_basildi(self):
        self.close()
        self.giris_ekrani = GirisEkrani()
        self.giris_ekrani.show()


if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    pencere = GirisEkrani()
    pencere.show()
    sys.exit(uygulama.exec_())
