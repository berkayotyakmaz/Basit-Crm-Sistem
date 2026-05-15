"""
Login Penceresi - Modern corporate tarzi. Koyu sol panel + sag form.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient, QBrush

from backend import AuthYoneticisi


class _SolPanel(QWidget):
    """Login sol panel - koyu lacivert gradient arka plan."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(520)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Gradient arka plan (koyu lacivert)
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0, QColor("#0f172a"))
        grad.setColorAt(1, QColor("#1e293b"))
        p.fillRect(self.rect(), QBrush(grad))

        margin = 48

        # Mavi accent noktasi + logo
        p.setBrush(QColor("#3b82f6"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(margin, 60, 8, 8), 4, 4)

        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 28, QFont.ExtraBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        p.setFont(font)
        p.drawText(QRectF(margin + 16, 48, w - margin * 2, 36),
                   Qt.AlignLeft | Qt.AlignVCenter, "Musteri Defteri")

        # Alt etiket
        p.setPen(QColor("#94a3b8"))
        font = QFont("Inter", 10, QFont.DemiBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.drawText(QRectF(margin + 16, 90, w - margin * 2, 18),
                   Qt.AlignLeft, "CRM SISTEMI")

        # Ince ayrac
        p.setPen(QPen(QColor(255, 255, 255, 30), 1))
        p.drawLine(margin, 128, w - margin, 128)

        # Slogan
        p.setPen(QColor("#e2e8f0"))
        font = QFont("Inter", 20, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.5)
        p.setFont(font)
        p.drawText(QRectF(margin, 170, w - margin * 2, 30),
                   Qt.AlignLeft, "Musterini tani,")
        p.drawText(QRectF(margin, 204, w - margin * 2, 30),
                   Qt.AlignLeft, "iliskini guclendir.")

        # Ozellikler
        ozellik_y = 280
        ozellikler = [
            "Musteri kayitlari ve takibi",
            "Satis yonetimi ve raporlama",
            "Destek talepleri takibi",
            "Detayli analizler ve grafikler",
        ]

        for i, oz in enumerate(ozellikler):
            y = ozellik_y + i * 40

            # Mavi bullet (daire)
            p.setBrush(QColor("#3b82f6"))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(QRectF(margin, y - 5, 6, 6), 3, 3)

            # Metin
            p.setPen(QColor("#cbd5e1"))
            font = QFont("Inter", 13)
            font.setWeight(QFont.Medium)
            p.setFont(font)
            p.drawText(margin + 20, y, oz)

        # Alt footer
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        p.drawLine(margin, h - 48, w - margin, h - 48)

        p.setPen(QColor("#64748b"))
        font = QFont("Inter", 9)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        p.setFont(font)
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "2026 Musteri Defteri")
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignRight | Qt.AlignVCenter, "v1.0")


class LoginPenceresi(QDialog):
    """Modern login dialog."""

    def __init__(self, auth: AuthYoneticisi, parent=None):
        super().__init__(parent)
        self.auth = auth
        self.dogrulanan_kullanici = None

        self.setWindowTitle("Musteri Defteri - Giris")
        self.setFixedSize(1080, 680)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        ana.addWidget(_SolPanel())

        # Sag form alani
        sag = QFrame()
        sag.setStyleSheet("background-color: #f8fafc;")
        sag_layout = QVBoxLayout(sag)
        sag_layout.setContentsMargins(56, 64, 56, 48)
        sag_layout.setSpacing(0)

        # Mavi etiket
        kat = QLabel("GIRIS YAP")
        kat.setStyleSheet(
            "color: #3b82f6; font-family: 'Inter', sans-serif; "
            "font-size: 10px; font-weight: 700; "
            "letter-spacing: 2px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(kat)
        sag_layout.addSpacing(14)

        baslik = QLabel("Hos Geldin")
        baslik.setStyleSheet(
            "color: #1e293b; font-family: 'Inter', 'Segoe UI', sans-serif; "
            "font-size: 36px; font-weight: 800; letter-spacing: -0.5px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(baslik)

        alt = QLabel("Devam etmek icin hesabina giris yap.")
        alt.setStyleSheet(
            "color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 14px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(alt)

        sag_layout.addSpacing(28)

        # Form
        sag_layout.addWidget(self._etiket("KULLANICI ADI"))
        sag_layout.addSpacing(6)

        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("kullanici adinizi girin")
        self.kul_input.setFixedHeight(46)
        self.kul_input.setStyleSheet(self._input_stil())
        self.kul_input.returnPressed.connect(lambda: self.sifre_input.setFocus())
        sag_layout.addWidget(self.kul_input)
        sag_layout.addSpacing(18)

        sag_layout.addWidget(self._etiket("SIFRE"))
        sag_layout.addSpacing(6)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("********")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setFixedHeight(46)
        self.sifre_input.setStyleSheet(self._input_stil())
        self.sifre_input.returnPressed.connect(self._giris_yap)
        sag_layout.addWidget(self.sifre_input)

        sag_layout.addSpacing(12)

        self.goster_chk = QCheckBox("Sifreyi goster")
        self.goster_chk.setStyleSheet(
            "QCheckBox { color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none; spacing: 8px; }"
            "QCheckBox::indicator { width: 14px; height: 14px; "
            "border: 1px solid #cbd5e1; border-radius: 3px; "
            "background-color: #ffffff; }"
            "QCheckBox::indicator:checked { background-color: #3b82f6; "
            "border: 1px solid #3b82f6; }"
        )
        self.goster_chk.toggled.connect(self._sifre_goster)
        sag_layout.addWidget(self.goster_chk)

        sag_layout.addSpacing(20)

        # Hata kutusu
        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fee2e2; color: #991b1b; "
            "border: 1px solid #fecaca; border-radius: 6px; "
            "padding: 12px 16px; "
            "font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        sag_layout.addWidget(self.hata_lbl)

        # Giris butonu
        self.giris_btn = QPushButton("GIRIS YAP")
        self.giris_btn.setFixedHeight(50)
        self.giris_btn.setCursor(Qt.PointingHandCursor)
        self.giris_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #ffffff; "
            "border: none; border-radius: 8px; "
            "font-family: 'Inter', sans-serif; font-size: 13px; "
            "font-weight: 700; } "
            "QPushButton:hover { background-color: #1d4ed8; }"
        )
        self.giris_btn.clicked.connect(self._giris_yap)
        sag_layout.addWidget(self.giris_btn)

        sag_layout.addSpacing(20)

        # Ipucu
        ipucu = QLabel(
            "<span style=\"color:#64748b; font-family:'Inter',sans-serif; "
            "font-size:11px; font-weight:600;\">VARSAYILAN ERISIM</span><br><br>"
            "<span style=\"color:#1e293b; font-family:'Inter',sans-serif; "
            "font-size:13px; font-weight:600;\">"
            "admin <span style='color:#3b82f6;'>&bull;</span> admin123</span>"
        )
        ipucu.setStyleSheet(
            "background-color: #eff6ff; "
            "border-left: 3px solid #3b82f6; "
            "padding: 14px 18px; border-radius: 6px;"
        )
        sag_layout.addWidget(ipucu)

        sag_layout.addStretch()

        footer = QLabel("2026 Musteri Defteri")
        footer.setStyleSheet(
            "color: #94a3b8; font-family: 'Inter', sans-serif; "
            "font-size: 10px; letter-spacing: 0.5px; "
            "background: transparent; border: none;"
        )
        footer.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(footer)

        ana.addWidget(sag, 1)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #334155; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; letter-spacing: 0.5px; "
            "background: transparent; border: none;"
        )
        return lbl

    def _input_stil(self) -> str:
        return (
            "QLineEdit { background-color: #ffffff; "
            "border: 1px solid #e2e8f0; "
            "border-radius: 8px; padding: 0 14px; "
            "color: #1e293b; font-family: 'Inter', sans-serif; font-size: 14px; "
            "selection-background-color: #3b82f6; selection-color: #ffffff; } "
            "QLineEdit:focus { border: 1.5px solid #3b82f6; "
            "background-color: #ffffff; } "
            "QLineEdit:hover { border: 1px solid #94a3b8; }"
        )

    def _sifre_goster(self, checked: bool):
        self.sifre_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )

    def _hata_goster(self, mesaj: str):
        self.hata_lbl.setText(mesaj)
        self.hata_lbl.setVisible(True)

    def _hata_gizle(self):
        self.hata_lbl.setVisible(False)

    def _giris_yap(self):
        kul = self.kul_input.text().strip()
        sifre = self.sifre_input.text()

        if not kul:
            self._hata_goster("Kullanici adi bos olamaz.")
            self.kul_input.setFocus()
            return
        if not sifre:
            self._hata_goster("Sifre bos olamaz.")
            self.sifre_input.setFocus()
            return

        kullanici = self.auth.dogrula(kul, sifre)
        if kullanici is None:
            self._hata_goster("Kullanici adi veya sifre hatali.")
            self.sifre_input.clear()
            self.sifre_input.setFocus()
            return

        self.dogrulanan_kullanici = kullanici
        self.accept()
