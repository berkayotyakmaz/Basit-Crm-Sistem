"""
Musteri Detay sayfasi - Tek musteri gorunumu.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTabWidget,
    QFrame,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    MuhurAvatar,
    MetrikKart,
    Rozet,
    OncelikRozet,
    DurumRozeti,
    HucreSarmalayici,
    format_para,
    format_telefon,
)


class MusteriDetaySayfasi(QWidget):
    geri_signal = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.musteri_id = None
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        self.ana_layout = QVBoxLayout(self)
        self.ana_layout.setContentsMargins(40, 32, 40, 32)
        self.ana_layout.setSpacing(16)

        # Geri butonu
        geri = QPushButton("< GERI")
        geri.setObjectName("HayaletButon")
        geri.setFixedHeight(32)
        geri.setFixedWidth(100)
        geri.setCursor(Qt.PointingHandCursor)
        geri.clicked.connect(self.geri_signal.emit)
        self.ana_layout.addWidget(geri)

        # Ust bilgi
        ust = QHBoxLayout()
        ust.setSpacing(20)

        self.avatar = MuhurAvatar("?", boyut=64)
        ust.addWidget(self.avatar, 0, Qt.AlignTop)

        bilgi = QVBoxLayout()
        bilgi.setSpacing(4)

        self.ad_lbl = QLabel("")
        self.ad_lbl.setStyleSheet(
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 32px; font-weight: 900; color: #0e0e0c; "
            "background: transparent; border: none; letter-spacing: -0.5px;"
        )
        bilgi.addWidget(self.ad_lbl)

        self.firma_lbl = QLabel("")
        self.firma_lbl.setStyleSheet(
            "font-family: 'Inter', sans-serif; font-size: 14px; "
            "color: #7a7a72; font-style: italic; "
            "background: transparent; border: none;"
        )
        bilgi.addWidget(self.firma_lbl)

        detay_satir = QHBoxLayout()
        detay_satir.setSpacing(20)

        self.telefon_lbl = QLabel("")
        self.telefon_lbl.setStyleSheet(
            "font-family: 'Inter', sans-serif; font-size: 12px; "
            "color: #3d3d3a; background: transparent; border: none;"
        )
        detay_satir.addWidget(self.telefon_lbl)

        self.email_lbl = QLabel("")
        self.email_lbl.setStyleSheet(
            "font-family: 'Inter', sans-serif; font-size: 12px; "
            "color: #3d3d3a; background: transparent; border: none;"
        )
        detay_satir.addWidget(self.email_lbl)

        self.kayit_lbl = QLabel("")
        self.kayit_lbl.setStyleSheet(
            "font-family: 'Inter', sans-serif; font-size: 12px; "
            "color: #7a7a72; background: transparent; border: none;"
        )
        detay_satir.addWidget(self.kayit_lbl)
        detay_satir.addStretch()

        bilgi.addLayout(detay_satir)
        ust.addLayout(bilgi, 1)
        self.ana_layout.addLayout(ust)

        # Ayrac
        ayrac = QFrame()
        ayrac.setFixedHeight(2)
        ayrac.setStyleSheet("background-color: #0e0e0c;")
        self.ana_layout.addWidget(ayrac)

        # Metrik kartlar
        metrik_satir = QHBoxLayout()
        metrik_satir.setSpacing(16)

        self.kart_satis = MetrikKart("Toplam Satis")
        self.kart_harcama = MetrikKart("Toplam Harcama", accent=True)
        self.kart_talep = MetrikKart("Acik Talep")

        metrik_satir.addWidget(self.kart_satis)
        metrik_satir.addWidget(self.kart_harcama)
        metrik_satir.addWidget(self.kart_talep)
        self.ana_layout.addLayout(metrik_satir)

        # Tab widget
        self.tab = QTabWidget()

        # Satis gecmisi
        satis_w = QWidget()
        satis_l = QVBoxLayout(satis_w)
        satis_l.setContentsMargins(0, 12, 0, 0)
        self.satis_tablo = QTableWidget()
        self.satis_tablo.setColumnCount(4)
        self.satis_tablo.setHorizontalHeaderLabels(["URUN", "FIYAT", "ADET", "TARIH"])
        self.satis_tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.satis_tablo.verticalHeader().setVisible(False)
        self.satis_tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.satis_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.satis_tablo.setAlternatingRowColors(True)
        satis_l.addWidget(self.satis_tablo)
        self.tab.addTab(satis_w, "SATIS GECMISI")

        # Destek talepleri
        talep_w = QWidget()
        talep_l = QVBoxLayout(talep_w)
        talep_l.setContentsMargins(0, 12, 0, 0)
        self.talep_tablo = QTableWidget()
        self.talep_tablo.setColumnCount(4)
        self.talep_tablo.setHorizontalHeaderLabels(["ACIKLAMA", "ONCELIK", "DURUM", "TARIH"])
        self.talep_tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.talep_tablo.verticalHeader().setVisible(False)
        self.talep_tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.talep_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.talep_tablo.setAlternatingRowColors(True)
        talep_l.addWidget(self.talep_tablo)
        self.tab.addTab(talep_w, "DESTEK TALEPLERI")

        self.ana_layout.addWidget(self.tab, 1)

    def musteri_goster(self, musteri_id: int):
        self.musteri_id = musteri_id
        self.yenile()

    def yenile(self):
        if not self.musteri_id:
            return

        m = self.vy.musteri_bul(self.musteri_id)
        if not m:
            return

        # Avatar guncelle
        self.ana_layout.itemAt(1).layout().itemAt(0).widget().deleteLater()
        yeni_avatar = MuhurAvatar(m.ad, boyut=64)
        self.ana_layout.itemAt(1).layout().insertWidget(0, yeni_avatar, 0, Qt.AlignTop)

        self.ad_lbl.setText(m.ad)
        self.firma_lbl.setText(m.firma if m.firma else "Bireysel Musteri")
        self.telefon_lbl.setText("Tel: " + format_telefon(m.telefon))
        self.email_lbl.setText("E-posta: " + (m.email or "-"))
        self.kayit_lbl.setText("Kayit: " + m.kayit_tarihi)

        # Metrikler
        satislar = [s for s in self.vy.tum_satislar() if s.musteri_id == m.musteri_id]
        harcama = sum(s.toplam_tutar() for s in satislar)
        acik_talep = self.vy.musteri_acik_talep_sayisi(m.musteri_id)

        self.kart_satis.deger_ayarla(str(len(satislar)))
        self.kart_harcama.deger_ayarla(format_para(harcama))
        self.kart_talep.deger_ayarla(str(acik_talep))

        # Satis tablosu
        self.satis_tablo.setRowCount(len(satislar))
        for i, s in enumerate(satislar):
            self.satis_tablo.setItem(i, 0, QTableWidgetItem(s.urun))
            tutar = QTableWidgetItem(format_para(s.toplam_tutar()))
            tutar.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.satis_tablo.setItem(i, 1, tutar)
            self.satis_tablo.setItem(i, 2, QTableWidgetItem(str(s.adet)))
            self.satis_tablo.setItem(i, 3, QTableWidgetItem(s.tarih))
            self.satis_tablo.setRowHeight(i, 44)

        # Talep tablosu
        talepler = [t for t in self.vy.tum_talepler() if t.musteri_id == m.musteri_id]
        self.talep_tablo.setRowCount(len(talepler))
        for i, t in enumerate(talepler):
            self.talep_tablo.setItem(i, 0, QTableWidgetItem(t.aciklama[:80]))
            self.talep_tablo.setCellWidget(i, 1, HucreSarmalayici(OncelikRozet(t.oncelik)))
            self.talep_tablo.setCellWidget(i, 2, HucreSarmalayici(DurumRozeti(t.durum)))
            self.talep_tablo.setItem(i, 3, QTableWidgetItem(t.olusturma_tarihi))
            self.talep_tablo.setRowHeight(i, 48)
