"""
Destek Talepleri sayfasi - Durum filtresi, oncelik rozeti, cevapla/kapat.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    OncelikRozet,
    DurumRozeti,
    HucreSarmalayici,
)
from frontend.widgets.diyaloglar import TalepDiyalog, CevaplaDiyalog


# ─── Inline buton stilleri (tablo icinde QSS cakismasini onler) ───

STIL_MAVI_BTN = (
    "QPushButton { background-color: #3b82f6; color: #ffffff; "
    "border: none; border-radius: 4px; padding: 4px 8px; " # Padding daraltıldı
    "font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 700; } "
    "QPushButton:hover { background-color: #1d4ed8; }"
)

STIL_KIRMIZI_BTN = (
    "QPushButton { background-color: #ffffff; color: #ef4444; "
    "border: 1px solid #fecaca; border-radius: 4px; padding: 4px 12px; "
    "font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 700; } "
    "QPushButton:hover { background-color: #ef4444; color: #ffffff; "
    "border: 1px solid #ef4444; }"
)


class TaleplerSayfasi(QWidget):
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
            "DESTEK",
            "Destek Talepleri",
            "Musteri destek taleplerini takip edin ve yonetin.",
        )
        layout.addWidget(header)

        # Filtre bar
        bar = QHBoxLayout()
        bar.setSpacing(12)

        self.durum_combo = QComboBox()
        self.durum_combo.setFixedHeight(40)
        self.durum_combo.setFixedWidth(160)
        self.durum_combo.addItem("Tumu", "tumu")
        self.durum_combo.addItem("Acik", "acik")
        self.durum_combo.addItem("Cevaplandi", "cevaplandi")
        self.durum_combo.addItem("Kapali", "kapali")
        self.durum_combo.currentIndexChanged.connect(lambda: self._filtrele())
        bar.addWidget(self.durum_combo)

        bar.addStretch()

        self.ekle_btn = QPushButton("YENI TALEP")
        self.ekle_btn.setObjectName("PrimaryButon")
        self.ekle_btn.setStyleSheet("background-color: #3b82f6; color: #ffffff; border: none; font-weight: bold; border-radius: 4px;")
        self.ekle_btn.setFixedHeight(40)
        self.ekle_btn.setCursor(Qt.PointingHandCursor)
        self.ekle_btn.clicked.connect(self._talep_ekle)
        bar.addWidget(self.ekle_btn)

        layout.addLayout(bar)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels([
            "MUSTERI", "ACIKLAMA", "ONCELIK", "DURUM", "TARIH", "ISLEM"
        ])
        self.tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tablo.setColumnWidth(0, 140)
        self.tablo.setColumnWidth(2, 110)
        self.tablo.setColumnWidth(3, 120)
        self.tablo.setColumnWidth(4, 100)
        self.tablo.setColumnWidth(5, 240)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setAlternatingRowColors(True)
        layout.addWidget(self.tablo)

    def yenile(self):
        self._filtrele()

    def _filtrele(self):
        talepler = self.vy.tum_talepler()
        durum = self.durum_combo.currentData()

        if durum and durum != "tumu":
            talepler = [t for t in talepler if t.durum == durum]

        self.tablo.setRowCount(len(talepler))
        for i, t in enumerate(talepler):
            m = self.vy.musteri_bul(t.musteri_id)
            self.tablo.setItem(i, 0, QTableWidgetItem(m.ad if m else "?"))
            self.tablo.setItem(i, 1, QTableWidgetItem(t.aciklama[:80]))
            self.tablo.setCellWidget(i, 2, HucreSarmalayici(OncelikRozet(t.oncelik)))
            self.tablo.setCellWidget(i, 3, HucreSarmalayici(DurumRozeti(t.durum)))
            self.tablo.setItem(i, 4, QTableWidgetItem(t.olusturma_tarihi))

            # Islem butonlari — inline stil ile
            btn_w = QWidget()
            btn_w.setStyleSheet("background: transparent;")
            btn_l = QHBoxLayout(btn_w)
            btn_l.setContentsMargins(4, 4, 4, 4)
            btn_l.setSpacing(6)

            if t.durum == "acik":
                cevapla = QPushButton("CEVAPLA")
                cevapla.setStyleSheet(STIL_MAVI_BTN)
                cevapla.setFixedHeight(28)
                cevapla.setCursor(Qt.PointingHandCursor)
                cevapla.clicked.connect(lambda _, tid=t.talep_id: self._cevapla(tid))
                btn_l.addWidget(cevapla)

            if t.durum != "kapali":
                kapat = QPushButton("KAPAT")
                kapat.setStyleSheet(STIL_KIRMIZI_BTN)
                kapat.setFixedHeight(28)
                kapat.setCursor(Qt.PointingHandCursor)
                kapat.clicked.connect(lambda _, tid=t.talep_id: self._kapat(tid))
                btn_l.addWidget(kapat)

            btn_l.addStretch()
            self.tablo.setCellWidget(i, 5, btn_w)
            self.tablo.setRowHeight(i, 48)

    def _talep_ekle(self):
        musteriler = self.vy.tum_musteriler()
        if not musteriler:
            QMessageBox.warning(self, "Hata", "Once musteri eklemelisiniz.")
            return
        dlg = TalepDiyalog(musteriler, self)
        if dlg.exec_() == TalepDiyalog.Accepted:
            veri = dlg.veri_al()
            try:
                self.vy.talep_ekle(**veri)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def _cevapla(self, talep_id: int):
        t = self.vy.talep_bul(talep_id)
        if not t:
            return
        m = self.vy.musteri_bul(t.musteri_id)
        musteri_ad = m.ad if m else "?"

        dlg = CevaplaDiyalog(t, musteri_ad=musteri_ad, parent=self)
        if dlg.exec_() == CevaplaDiyalog.Accepted:
            yanit = dlg.yanit_al()
            try:
                self.vy.talep_cevapla(talep_id)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def _kapat(self, talep_id: int):
        cevap = QMessageBox.question(
            self, "Talebi Kapat",
            "Bu talebi kapatmak istediginize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.talep_kapat(talep_id)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))
