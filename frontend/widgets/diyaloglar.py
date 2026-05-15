"""
Diyaloglar - MusteriDiyalog, SatisDiyalog, TalepDiyalog.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QFrame,
    QSpinBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class _BaseDiyalog(QDialog):
    """Temel diyalog altyapisi."""

    def __init__(self, baslik: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(baslik)
        self.setMinimumWidth(480)
        self.setModal(True)

        self.ana_layout = QVBoxLayout(self)
        self.ana_layout.setContentsMargins(32, 28, 32, 24)
        self.ana_layout.setSpacing(0)

        # Baslik
        kat = QLabel(baslik)
        kat.setStyleSheet(
            "color: #1e293b; font-family: 'Inter', sans-serif; "
            "font-size: 18px; font-weight: 700; "
            "background: transparent; border: none;"
        )
        self.ana_layout.addWidget(kat)
        self.ana_layout.addSpacing(6)

        ayrac = QFrame()
        ayrac.setFixedHeight(1)
        ayrac.setStyleSheet("background-color: #e2e8f0;")
        self.ana_layout.addWidget(ayrac)
        self.ana_layout.addSpacing(20)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #334155; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        return lbl

    def _input(self, placeholder: str = "") -> QLineEdit:
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(40)
        return inp

    def _butonlar_ekle(self, kaydet_metin: str = "KAYDET"):
        self.ana_layout.addSpacing(20)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        iptal = QPushButton("IPTAL")
        iptal.setObjectName("HayaletButon")
        iptal.setFixedHeight(42)
        iptal.setCursor(Qt.PointingHandCursor)
        iptal.clicked.connect(self.reject)
        btn_layout.addWidget(iptal)

        self.kaydet_btn = QPushButton(kaydet_metin)
        self.kaydet_btn.setObjectName("PrimaryButon")
        self.kaydet_btn.setFixedHeight(42)
        self.kaydet_btn.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.kaydet_btn)

        self.ana_layout.addLayout(btn_layout)


class MusteriDiyalog(_BaseDiyalog):
    """Musteri ekleme/duzenleme diyalogu."""

    def __init__(self, parent=None, musteri=None):
        baslik = "Musteri Duzenle" if musteri else "Yeni Musteri"
        super().__init__(baslik, parent)
        self.musteri = musteri

        self.ana_layout.addWidget(self._etiket("AD SOYAD"))
        self.ana_layout.addSpacing(6)
        self.ad_input = self._input("Musteri adi")
        self.ana_layout.addWidget(self.ad_input)
        self.ana_layout.addSpacing(14)

        self.ana_layout.addWidget(self._etiket("TELEFON"))
        self.ana_layout.addSpacing(6)
        self.telefon_input = self._input("05XX XXX XX XX")
        self.ana_layout.addWidget(self.telefon_input)
        self.ana_layout.addSpacing(14)

        self.ana_layout.addWidget(self._etiket("E-POSTA"))
        self.ana_layout.addSpacing(6)
        self.email_input = self._input("ornek@mail.com")
        self.ana_layout.addWidget(self.email_input)
        self.ana_layout.addSpacing(14)

        self.ana_layout.addWidget(self._etiket("FIRMA"))
        self.ana_layout.addSpacing(6)
        self.firma_input = self._input("Firma adi (opsiyonel)")
        self.ana_layout.addWidget(self.firma_input)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "color: #ef4444; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        self.hata_lbl.setVisible(False)
        self.ana_layout.addSpacing(8)
        self.ana_layout.addWidget(self.hata_lbl)

        self._butonlar_ekle()
        self.kaydet_btn.clicked.connect(self._dogrula)

        if musteri:
            self.ad_input.setText(musteri.ad)
            self.telefon_input.setText(musteri.telefon)
            self.email_input.setText(musteri.email)
            self.firma_input.setText(musteri.firma)

    def _dogrula(self):
        if not self.ad_input.text().strip():
            self.hata_lbl.setText("Ad bos olamaz.")
            self.hata_lbl.setVisible(True)
            return
        tel = "".join(c for c in self.telefon_input.text() if c.isdigit())
        if len(tel) < 10 or len(tel) > 11:
            self.hata_lbl.setText("Telefon 10-11 haneli olmali.")
            self.hata_lbl.setVisible(True)
            return
        self.accept()

    def veri_al(self) -> dict:
        return {
            "ad": self.ad_input.text().strip(),
            "telefon": self.telefon_input.text().strip(),
            "email": self.email_input.text().strip(),
            "firma": self.firma_input.text().strip(),
        }


class SatisDiyalog(_BaseDiyalog):
    """Satis ekleme diyalogu."""

    def __init__(self, musteriler: list, parent=None):
        super().__init__("Yeni Satis", parent)
        self.musteriler = musteriler

        self.ana_layout.addWidget(self._etiket("MUSTERI"))
        self.ana_layout.addSpacing(6)
        self.musteri_combo = QComboBox()
        self.musteri_combo.setFixedHeight(40)
        for m in musteriler:
            etiket = m.ad
            if m.firma:
                etiket += f" ({m.firma})"
            self.musteri_combo.addItem(etiket, m.musteri_id)
        self.ana_layout.addWidget(self.musteri_combo)
        self.ana_layout.addSpacing(14)

        self.ana_layout.addWidget(self._etiket("URUN"))
        self.ana_layout.addSpacing(6)
        self.urun_input = self._input("Urun adi")
        self.ana_layout.addWidget(self.urun_input)
        self.ana_layout.addSpacing(14)

        satir = QHBoxLayout()
        satir.setSpacing(14)

        sol = QVBoxLayout()
        sol.addWidget(self._etiket("FIYAT (TL)"))
        sol.addSpacing(6)
        self.fiyat_input = self._input("0.00")
        sol.addWidget(self.fiyat_input)
        satir.addLayout(sol)

        sag = QVBoxLayout()
        sag.addWidget(self._etiket("ADET"))
        sag.addSpacing(6)
        self.adet_spin = QSpinBox()
        self.adet_spin.setFixedHeight(40)
        self.adet_spin.setMinimum(1)
        self.adet_spin.setMaximum(9999)
        self.adet_spin.setValue(1)
        sag.addWidget(self.adet_spin)
        satir.addLayout(sag)

        self.ana_layout.addLayout(satir)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "color: #ef4444; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        self.hata_lbl.setVisible(False)
        self.ana_layout.addSpacing(8)
        self.ana_layout.addWidget(self.hata_lbl)

        self._butonlar_ekle()
        self.kaydet_btn.clicked.connect(self._dogrula)

    def _dogrula(self):
        if not self.urun_input.text().strip():
            self.hata_lbl.setText("Urun adi bos olamaz.")
            self.hata_lbl.setVisible(True)
            return
        try:
            fiyat = float(self.fiyat_input.text().replace(",", "."))
            if fiyat <= 0:
                raise ValueError
        except ValueError:
            self.hata_lbl.setText("Gecerli bir fiyat girin.")
            self.hata_lbl.setVisible(True)
            return
        self.accept()

    def veri_al(self) -> dict:
        return {
            "musteri_id": self.musteri_combo.currentData(),
            "urun": self.urun_input.text().strip(),
            "fiyat": float(self.fiyat_input.text().replace(",", ".")),
            "adet": self.adet_spin.value(),
        }


class TalepDiyalog(_BaseDiyalog):
    """Destek talebi ekleme diyalogu."""

    def __init__(self, musteriler: list, parent=None):
        super().__init__("Yeni Destek Talebi", parent)
        self.musteriler = musteriler

        self.ana_layout.addWidget(self._etiket("MUSTERI"))
        self.ana_layout.addSpacing(6)
        self.musteri_combo = QComboBox()
        self.musteri_combo.setFixedHeight(40)
        for m in musteriler:
            etiket = m.ad
            if m.firma:
                etiket += f" ({m.firma})"
            self.musteri_combo.addItem(etiket, m.musteri_id)
        self.ana_layout.addWidget(self.musteri_combo)
        self.ana_layout.addSpacing(14)

        self.ana_layout.addWidget(self._etiket("ONCELIK"))
        self.ana_layout.addSpacing(6)
        self.oncelik_combo = QComboBox()
        self.oncelik_combo.setFixedHeight(40)
        self.oncelik_combo.addItem("Dusuk", "dusuk")
        self.oncelik_combo.addItem("Orta", "orta")
        self.oncelik_combo.addItem("Yuksek", "yuksek")
        self.oncelik_combo.setCurrentIndex(1)
        self.ana_layout.addWidget(self.oncelik_combo)
        self.ana_layout.addSpacing(14)

        self.ana_layout.addWidget(self._etiket("ACIKLAMA"))
        self.ana_layout.addSpacing(6)
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setFixedHeight(100)
        self.aciklama_input.setPlaceholderText("Sorunu aciklayiniz...")
        self.ana_layout.addWidget(self.aciklama_input)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "color: #ef4444; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        self.hata_lbl.setVisible(False)
        self.ana_layout.addSpacing(8)
        self.ana_layout.addWidget(self.hata_lbl)

        self._butonlar_ekle()
        self.kaydet_btn.clicked.connect(self._dogrula)

    def _dogrula(self):
        if not self.aciklama_input.toPlainText().strip():
            self.hata_lbl.setText("Aciklama bos olamaz.")
            self.hata_lbl.setVisible(True)
            return
        self.accept()

    def veri_al(self) -> dict:
        return {
            "musteri_id": self.musteri_combo.currentData(),
            "aciklama": self.aciklama_input.toPlainText().strip(),
            "oncelik": self.oncelik_combo.currentData(),
        }


class CevaplaDiyalog(_BaseDiyalog):
    """Destek talebine yanit verme diyalogu."""

    def __init__(self, talep, musteri_ad: str = "", parent=None):
        super().__init__("Talebe Yanit Ver", parent)
        self.talep = talep

        # Talep bilgisi
        bilgi = QLabel(f"Musteri: {musteri_ad}")
        bilgi.setStyleSheet(
            "color: #1e293b; font-family: 'Inter', sans-serif; "
            "font-size: 13px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        self.ana_layout.addWidget(bilgi)
        self.ana_layout.addSpacing(6)

        talep_metin = QLabel(f'"{talep.aciklama}"')
        talep_metin.setWordWrap(True)
        talep_metin.setStyleSheet(
            "color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 12px; font-style: italic; "
            "background-color: #f1f5f9; border: none; border-radius: 6px; "
            "padding: 12px 14px;"
        )
        self.ana_layout.addWidget(talep_metin)
        self.ana_layout.addSpacing(16)

        self.ana_layout.addWidget(self._etiket("YANITINIZ"))
        self.ana_layout.addSpacing(6)
        self.yanit_input = QTextEdit()
        self.yanit_input.setFixedHeight(120)
        self.yanit_input.setPlaceholderText("Yanitinizi yaziniz...")
        self.ana_layout.addWidget(self.yanit_input)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "color: #ef4444; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        self.hata_lbl.setVisible(False)
        self.ana_layout.addSpacing(8)
        self.ana_layout.addWidget(self.hata_lbl)

        self._butonlar_ekle("YANIT GONDER")
        self.kaydet_btn.clicked.connect(self._dogrula)

    def _dogrula(self):
        if not self.yanit_input.toPlainText().strip():
            self.hata_lbl.setText("Yanit bos olamaz.")
            self.hata_lbl.setVisible(True)
            return
        self.accept()

    def yanit_al(self) -> str:
        return self.yanit_input.toPlainText().strip()
