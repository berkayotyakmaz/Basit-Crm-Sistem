"""
Satislar sayfasi - Tum satislar tablosu, filtreler.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime, timedelta

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    format_para,
    HucreSarmalayici,
)
from frontend.widgets.diyaloglar import SatisDiyalog


class SatislarSayfasi(QWidget):
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(16)

        header = EditorialHeader(
            "SATISLAR",
            "Satislar",
            "Tum satis kayitlarini goruntuleyin ve yonetin.",
        )
        layout.addWidget(header)

        # Filtre bar
        bar = QHBoxLayout()
        bar.setSpacing(12)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("Urun veya musteri ara...")
        self.arama.setFixedHeight(40)
        self.arama.textChanged.connect(self._filtrele)
        bar.addWidget(self.arama, 1)

        self.tarih_combo = QComboBox()
        self.tarih_combo.setFixedHeight(40)
        self.tarih_combo.setFixedWidth(160)
        self.tarih_combo.addItem("Tum Zamanlar", 0)
        self.tarih_combo.addItem("Son 1 Hafta", 7)
        self.tarih_combo.addItem("Son 1 Ay", 30)
        self.tarih_combo.addItem("Son 3 Ay", 90)
        self.tarih_combo.currentIndexChanged.connect(lambda: self._filtrele())
        bar.addWidget(self.tarih_combo)

        self.ekle_btn = QPushButton("YENI SATIS")
        self.ekle_btn.setObjectName("PrimaryButon")
        self.ekle_btn.setStyleSheet("background-color: #3b82f6; color: #ffffff; border: none; font-weight: bold; border-radius: 4px;")
        self.ekle_btn.setFixedHeight(40)
        self.ekle_btn.setCursor(Qt.PointingHandCursor)
        self.ekle_btn.clicked.connect(self._satis_ekle)
        bar.addWidget(self.ekle_btn)

        layout.addLayout(bar)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels([
            "TARIH", "MUSTERI", "URUN", "FIYAT", "ADET", "TOPLAM"
        ])
        self.tablo.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tablo.setColumnWidth(0, 100)
        self.tablo.setColumnWidth(3, 120)
        self.tablo.setColumnWidth(4, 60)
        self.tablo.setColumnWidth(5, 140)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setAlternatingRowColors(True)
        layout.addWidget(self.tablo)

    def yenile(self):
        self._filtrele()

    def _filtrele(self, _=None):
        satislar = self.vy.tum_satislar()
        arama = self.arama.text().strip().lower()

        # Tarih filtresi
        gun = self.tarih_combo.currentData()
        if gun and gun > 0:
            bugun = datetime.now()
            sinir = bugun - timedelta(days=gun)
            filtreli = []
            for s in satislar:
                try:
                    t = datetime.strptime(s.tarih, "%d.%m.%Y")
                    if t >= sinir:
                        filtreli.append(s)
                except ValueError:
                    filtreli.append(s)
            satislar = filtreli

        # Arama filtresi
        if arama:
            filtreli = []
            for s in satislar:
                m = self.vy.musteri_bul(s.musteri_id)
                musteri_ad = m.ad.lower() if m else ""
                if arama in s.urun.lower() or arama in musteri_ad:
                    filtreli.append(s)
            satislar = filtreli

        # Tarihe gore sirala (yeniden eskiye)
        satislar.sort(key=lambda s: s.satis_id, reverse=True)

        self.tablo.setRowCount(len(satislar))
        for i, s in enumerate(satislar):
            m = self.vy.musteri_bul(s.musteri_id)

            self.tablo.setItem(i, 0, QTableWidgetItem(s.tarih))
            self.tablo.setItem(i, 1, QTableWidgetItem(m.ad if m else "?"))
            self.tablo.setItem(i, 2, QTableWidgetItem(s.urun))

            fiyat_item = QTableWidgetItem(format_para(s.fiyat))
            fiyat_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tablo.setItem(i, 3, fiyat_item)

            self.tablo.setItem(i, 4, QTableWidgetItem(str(s.adet)))

            toplam_item = QTableWidgetItem(format_para(s.toplam_tutar()))
            toplam_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tablo.setItem(i, 5, toplam_item)

            self.tablo.setRowHeight(i, 48)

    def _satis_ekle(self):
        musteriler = self.vy.tum_musteriler()
        if not musteriler:
            QMessageBox.warning(self, "Hata", "Once musteri eklemelisiniz.")
            return
        dlg = SatisDiyalog(musteriler, self)
        if dlg.exec_() == SatisDiyalog.Accepted:
            veri = dlg.veri_al()
            try:
                self.vy.satis_ekle(**veri)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))
