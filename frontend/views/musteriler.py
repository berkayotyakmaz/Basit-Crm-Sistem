"""
Musteriler sayfasi - Tablo, MuhurAvatar, telefon + harcama rozeti.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea,
    QFrame,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    MuhurAvatar,
    Rozet,
    HucreSarmalayici,
    format_para,
    format_telefon,
)
from frontend.widgets.diyaloglar import MusteriDiyalog


class MusterilerSayfasi(QWidget):
    veri_degisti = pyqtSignal()
    musteri_secildi = pyqtSignal(int)

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
            "MUSTERILER",
            "Musteriler",
            "Tum musteri kayitlarini goruntuleyin ve yonetin.",
        )
        layout.addWidget(header)

        # Ust bar: arama + butonlar
        bar = QHBoxLayout()
        bar.setSpacing(12)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("Musteri ara...")
        self.arama.setFixedHeight(40)
        self.arama.textChanged.connect(self._filtrele)
        bar.addWidget(self.arama, 1)

        self.ekle_btn = QPushButton("YENI MUSTERI")
        self.ekle_btn.setObjectName("PrimaryButon")
        self.ekle_btn.setStyleSheet("background-color: #3b82f6; color: #ffffff; border: none; font-weight: bold; border-radius: 4px;")
        self.ekle_btn.setFixedHeight(40)
        self.ekle_btn.setCursor(Qt.PointingHandCursor)
        self.ekle_btn.clicked.connect(self._musteri_ekle)
        bar.addWidget(self.ekle_btn)

        layout.addLayout(bar)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels([
            "", "AD SOYAD", "FIRMA", "TELEFON", "E-POSTA", "HARCAMA", "ISLEM"
        ])
        self.tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.tablo.setColumnWidth(0, 70)
        self.tablo.setColumnWidth(3, 150)
        self.tablo.setColumnWidth(5, 140)
        self.tablo.setColumnWidth(6, 200)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setAlternatingRowColors(True)
        layout.addWidget(self.tablo)

    def yenile(self):
        self._filtrele(self.arama.text())

    def _filtrele(self, arama: str = ""):
        musteriler = self.vy.tum_musteriler()
        if arama.strip():
            q = arama.strip().lower()
            musteriler = [m for m in musteriler
                          if q in m.ad.lower() or q in m.firma.lower()
                          or q in m.telefon or q in m.email.lower()]

        self.tablo.setRowCount(len(musteriler))
        for i, m in enumerate(musteriler):
            # Avatar
            avatar = MuhurAvatar(m.ad, boyut=32)
            self.tablo.setCellWidget(i, 0, HucreSarmalayici(avatar))

            self.tablo.setItem(i, 1, QTableWidgetItem(m.ad))
            self.tablo.setItem(i, 2, QTableWidgetItem(m.firma or "-"))
            self.tablo.setItem(i, 3, QTableWidgetItem(format_telefon(m.telefon)))
            self.tablo.setItem(i, 4, QTableWidgetItem(m.email or "-"))

            harcama = self.vy.musteri_toplam_harcama(m.musteri_id)
            tutar_item = QTableWidgetItem(format_para(harcama))
            tutar_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tablo.setItem(i, 5, tutar_item)

            # Islem butonlari — inline stil ile (tablo QSS cakismasini onler)
            btn_w = QWidget()
            btn_w.setStyleSheet("background: transparent;")
            btn_l = QHBoxLayout(btn_w)
            btn_l.setContentsMargins(4, 4, 4, 4)
            btn_l.setSpacing(4)

            STIL_MAVI = (
                "QPushButton { background-color: #3b82f6; color: #ffffff; "
                "border: none; border-radius: 4px; padding: 4px 6px; " 
                "font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 700; } "
                "QPushButton:hover { background-color: #1d4ed8; }"
            )
            STIL_KONTUR = (
                "QPushButton { background-color: #ffffff; color: #334155; "
                "border: 1px solid #94a3b8; border-radius: 4px; padding: 4px 6px; "
                "font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 700; } "
                "QPushButton:hover { background-color: #f1f5f9; border: 1px solid #64748b; }"
            )
            STIL_KIRMIZI = (
                "QPushButton { background-color: #ffffff; color: #ef4444; "
                "border: 1px solid #fecaca; border-radius: 4px; padding: 4px 6px; "
                "font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 700; } "
                "QPushButton:hover { background-color: #ef4444; color: #ffffff; "
                "border: 1px solid #ef4444; }"
            )

            detay_btn = QPushButton("DETAY")
            detay_btn.setStyleSheet(STIL_MAVI)
            detay_btn.setFixedHeight(28)
            detay_btn.setCursor(Qt.PointingHandCursor)
            detay_btn.clicked.connect(lambda _, mid=m.musteri_id: self.musteri_secildi.emit(mid))
            btn_l.addWidget(detay_btn)

            duzenle_btn = QPushButton("DUZENLE")
            duzenle_btn.setStyleSheet(STIL_KONTUR)
            duzenle_btn.setFixedHeight(28)
            duzenle_btn.setCursor(Qt.PointingHandCursor)
            duzenle_btn.clicked.connect(lambda _, mid=m.musteri_id: self._musteri_duzenle(mid))
            btn_l.addWidget(duzenle_btn)

            sil_btn = QPushButton("SIL")
            sil_btn.setStyleSheet(STIL_KIRMIZI)
            sil_btn.setFixedHeight(28)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.clicked.connect(lambda _, mid=m.musteri_id: self._musteri_sil(mid))
            btn_l.addWidget(sil_btn)

            self.tablo.setCellWidget(i, 6, btn_w)
            self.tablo.setRowHeight(i, 52)

    def _musteri_ekle(self):
        dlg = MusteriDiyalog(self)
        if dlg.exec_() == MusteriDiyalog.Accepted:
            veri = dlg.veri_al()
            try:
                self.vy.musteri_ekle(**veri)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def _musteri_duzenle(self, musteri_id: int):
        m = self.vy.musteri_bul(musteri_id)
        if not m:
            return
        dlg = MusteriDiyalog(self, musteri=m)
        if dlg.exec_() == MusteriDiyalog.Accepted:
            veri = dlg.veri_al()
            try:
                self.vy.musteri_guncelle(musteri_id, **veri)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))

    def _musteri_sil(self, musteri_id: int):
        cevap = QMessageBox.question(
            self, "Musteri Sil",
            "Bu musteriyi silmek istediginize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.musteri_sil(musteri_id)
                self.veri_degisti.emit()
                self.yenile()
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))
