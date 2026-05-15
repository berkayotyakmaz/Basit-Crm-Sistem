"""
Modern Corporate widget'lari - CRM sistemi icin.
Koyu sidebar, mavi accent, yuvarlatilmis koseler.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QFont,
    QFontMetrics,
    QLinearGradient,
)


# ─── Renk paleti ─────────────────────────────────────────

BG = QColor("#f8fafc")
BG_ALT = QColor("#f1f5f9")
CARD = QColor("#ffffff")
SIDEBAR = QColor("#0f172a")
SIDEBAR_HOVER = QColor("#1e293b")

TEXT = QColor("#1e293b")
TEXT_DIM = QColor("#334155")
TEXT_MUTED = QColor("#64748b")
TEXT_SUBTLE = QColor("#94a3b8")
TEXT_FAINT = QColor("#cbd5e1")

BORDER = QColor("#e2e8f0")
BORDER_LIGHT = QColor("#f1f5f9")

PRIMARY = QColor("#3b82f6")
PRIMARY_DARK = QColor("#1d4ed8")
PRIMARY_LIGHT = QColor("#dbeafe")

SUCCESS = QColor("#10b981")
SUCCESS_PALE = QColor("#d1fae5")
WARNING = QColor("#f59e0b")
WARNING_PALE = QColor("#fef3c7")
DANGER = QColor("#ef4444")
DANGER_PALE = QColor("#fee2e2")


# ─── Yardimci fonksiyonlar ────────────────────────────────

def format_para(tutar: float) -> str:
    """1234567.89 -> '1.234.567,89 TL'"""
    s = f"{tutar:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s + " TL"


def format_telefon(tel: str) -> str:
    """'05321234567' -> '0532 123 45 67'"""
    t = "".join(c for c in tel if c.isdigit())
    if len(t) == 11:
        return f"{t[:4]} {t[4:7]} {t[7:9]} {t[9:11]}"
    elif len(t) == 10:
        return f"{t[:3]} {t[3:6]} {t[6:8]} {t[8:10]}"
    return t


# ─── MetrikKart ───────────────────────────────────────────

class MetrikKart(QFrame):
    """Modern metrik kart - sol renkli serit + buyuk rakam."""

    def __init__(self, etiket: str, deger: str = "0", altyazi: str = "",
                 accent: bool = False, parent=None):
        super().__init__(parent)
        renk = "#3b82f6" if accent else "#e2e8f0"
        self.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e2e8f0; "
            f"border-left: 3px solid {renk}; "
            "border-radius: 8px; }"
        )
        self.setFixedHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        et = QLabel(etiket)
        et.setStyleSheet(
            "color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none;"
        )
        layout.addWidget(et)
        layout.addStretch()

        self.deger_lbl = QLabel(str(deger))
        self.deger_lbl.setStyleSheet(
            "color: #1e293b; "
            "font-family: 'Inter', 'Segoe UI', sans-serif; "
            "font-size: 32px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.deger_lbl)

        self.alt_lbl = QLabel(altyazi)
        self.alt_lbl.setStyleSheet(
            "color: #94a3b8; font-family: 'Inter', sans-serif; "
            "font-size: 11px; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.alt_lbl)

    def deger_ayarla(self, deger):
        deger_str = str(deger)
        n = len(deger_str)
        if n <= 3:
            size = 32
        elif n <= 6:
            size = 26
        elif n <= 10:
            size = 22
        else:
            size = 18
        self.deger_lbl.setStyleSheet(
            f"color: #1e293b; "
            f"font-family: 'Inter', 'Segoe UI', sans-serif; "
            f"font-size: {size}px; font-weight: 800; "
            f"background: transparent; border: none;"
        )
        self.deger_lbl.setText(deger_str)

    def altyazi_ayarla(self, altyazi):
        self.alt_lbl.setText(altyazi)


# ─── Masthead ─────────────────────────────────────────────

class Masthead(QWidget):
    """Sidebar ust logo: 'Musteri Defteri' + alt etiket."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Mavi accent noktasi
        p.setBrush(PRIMARY)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(22, 20, 6, 6), 3, 3)

        # Ana isim
        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", 17, QFont.ExtraBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.5)
        p.setFont(font)
        p.drawText(QRectF(34, 14, w - 56, 24),
                   Qt.AlignLeft | Qt.AlignVCenter, "Musteri Defteri")

        # Alt etiket
        p.setPen(TEXT_SUBTLE)
        font = QFont("Inter", 9, QFont.DemiBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(QRectF(34, 42, w - 56, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "CRM SISTEMI")

        # Alt cizgi
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        p.drawLine(22, h - 4, w - 22, h - 4)


# ─── PageHeader ──────────────────────────────────────────

class EditorialHeader(QWidget):
    """Sayfa ust header: kategori tag + baslik + altyazi."""

    def __init__(self, kategori: str, baslik: str, altyazi: str,
                 sag_etiket: str = "", sag_meta: str = "", parent=None):
        super().__init__(parent)
        self.kategori = kategori
        self.baslik = baslik
        self.altyazi = altyazi
        self.sag_etiket = sag_etiket
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Kategori tag (mavi)
        p.setPen(PRIMARY)
        font = QFont("Inter", 10, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(0, 24, self.kategori)

        # Buyuk baslik
        p.setPen(TEXT)
        font = QFont("Inter", 32, QFont.ExtraBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        p.setFont(font)
        p.drawText(QRectF(0, 36, w, 48),
                   Qt.AlignLeft | Qt.AlignVCenter, self.baslik)

        # Altyazi
        p.setPen(TEXT_MUTED)
        font = QFont("Inter", 13)
        p.setFont(font)
        p.drawText(QRectF(0, 88, w, 20),
                   Qt.AlignLeft | Qt.AlignVCenter, self.altyazi)

        # Alt ince cizgi
        p.setPen(QPen(BORDER, 1))
        p.drawLine(0, h - 1, w, h - 1)


# ─── MuhurAvatar ─────────────────────────────────────────

class MuhurAvatar(QWidget):
    """Modern daire avatar - bas harf + gradient arka plan."""

    PALETTES = [
        (QColor("#3b82f6"), QColor("#1d4ed8")),   # mavi
        (QColor("#8b5cf6"), QColor("#6d28d9")),   # mor
        (QColor("#10b981"), QColor("#047857")),   # yesil
        (QColor("#f59e0b"), QColor("#d97706")),   # amber
        (QColor("#ef4444"), QColor("#dc2626")),   # kirmizi
        (QColor("#06b6d4"), QColor("#0891b2")),   # cyan
        (QColor("#ec4899"), QColor("#db2777")),   # pembe
        (QColor("#6366f1"), QColor("#4f46e5")),   # indigo
    ]

    def __init__(self, ad: str, boyut: int = 40, parent=None):
        super().__init__(parent)
        self.ad = ad.strip()
        self.bas_harf = self.ad[0].upper() if self.ad else "?"
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        idx = hash(self.ad) % len(self.PALETTES)
        c1, c2 = self.PALETTES[idx]

        # Gradient daire
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0, c1)
        grad.setColorAt(1, c2)

        p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QRectF(0.5, 0.5, w - 1, h - 1))

        # Beyaz harf
        p.setPen(QColor("#ffffff"))
        font = QFont("Inter", int(w * 0.4), QFont.Bold)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.bas_harf)


# ─── ManseteKart ─────────────────────────────────────────

class ManseteKart(QWidget):
    """Dashboard hero kart - sol bilgi, sag 4 metrik."""

    def __init__(self, baslik: str, altyazi: str, by_line: str = "",
                 sag_metrikler: list = None, parent=None):
        super().__init__(parent)
        self.baslik = baslik
        self.altyazi = altyazi
        self.by_line = by_line
        self.sag_metrikler = sag_metrikler or []
        self.setMinimumHeight(240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def metrikleri_ayarla(self, metrikler: list):
        self.sag_metrikler = metrikler
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Kart arka plan (beyaz, hafif golge efekti icin border)
        p.setBrush(CARD)
        p.setPen(QPen(BORDER, 1))
        p.drawRoundedRect(QRectF(0, 0, w - 1, h - 1), 12, 12)

        # Ust mavi serit
        p.setBrush(PRIMARY)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(0, 0, w, 4), 2, 2)

        sol_x = 32
        sol_w = int(w * 0.55)

        # Kucuk etiket
        p.setPen(PRIMARY)
        font = QFont("Inter", 10, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(sol_x, 36, "GENEL BAKIS")

        # Baslik
        p.setPen(TEXT)
        font = QFont("Inter", 28, QFont.ExtraBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        p.setFont(font)

        fm = QFontMetrics(font)
        kelimeler = self.baslik.split()
        satirlar = []
        kalan = ""
        for k in kelimeler:
            test = kalan + (" " if kalan else "") + k
            if fm.horizontalAdvance(test) <= sol_w - 32:
                kalan = test
            else:
                if kalan:
                    satirlar.append(kalan)
                kalan = k
        if kalan:
            satirlar.append(kalan)
        satirlar = satirlar[:2]

        baslik_y = 56
        line_h = 38
        for i, satir in enumerate(satirlar):
            p.drawText(sol_x, baslik_y + (i + 1) * line_h, satir)

        # Altyazi
        alt_y = baslik_y + len(satirlar) * line_h + 16
        p.setPen(TEXT_MUTED)
        font = QFont("Inter", 13)
        p.setFont(font)

        fm = QFontMetrics(font)
        kelimeler = self.altyazi.split()
        alt_satirlar = []
        kalan = ""
        for k in kelimeler:
            test = kalan + (" " if kalan else "") + k
            if fm.horizontalAdvance(test) <= sol_w - 32:
                kalan = test
            else:
                if kalan:
                    alt_satirlar.append(kalan)
                kalan = k
        if kalan:
            alt_satirlar.append(kalan)
        alt_satirlar = alt_satirlar[:2]

        for i, satir in enumerate(alt_satirlar):
            p.drawText(sol_x, alt_y + i * 20, satir)

        # Dikey ayrac
        ayrac_x = int(w * 0.56)
        p.setPen(QPen(BORDER, 1))
        p.drawLine(ayrac_x, 24, ayrac_x, h - 24)

        # SAG TARAF - 4 metrik 2x2
        sag_x = ayrac_x + 32
        sag_w = w - sag_x - 32

        m = self.sag_metrikler[:4]
        if len(m) >= 4:
            cell_w = sag_w / 2
            cell_h = (h - 60) / 2
            grid_y = 30

            for i, (etiket, deger) in enumerate(m):
                row = i // 2
                col = i % 2
                cx = sag_x + col * cell_w
                cy = grid_y + row * cell_h

                # Etiket
                p.setPen(TEXT_MUTED)
                font = QFont("Inter", 9, QFont.DemiBold)
                font.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
                p.setFont(font)
                p.drawText(int(cx), int(cy + 16), etiket)

                # Deger
                p.setPen(TEXT)
                deger_str = str(deger)
                font_size = 28 if len(deger_str) <= 3 else (22 if len(deger_str) <= 6 else 18)
                font = QFont("Inter", font_size, QFont.ExtraBold)
                font.setLetterSpacing(QFont.AbsoluteSpacing, -0.5)
                p.setFont(font)
                p.drawText(int(cx), int(cy + 52), deger_str)

                # Mavi alt cizgi
                p.setBrush(PRIMARY)
                p.setPen(Qt.NoPen)
                p.drawRoundedRect(QRectF(cx, cy + 60, 24, 2), 1, 1)


# ─── KategoriBarYatay ─────────────────────────────────────

class KategoriBarYatay(QWidget):
    """Modern bar grafigi - renkli barlar."""

    def __init__(self, dagilim: dict, parent=None):
        super().__init__(parent)
        self.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.setMinimumHeight(n * 40 + 10)

    def paintEvent(self, e):
        if not self.dagilim:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        sirali = sorted(self.dagilim.items(), key=lambda x: -x[1])
        max_v = max(v for _, v in sirali) if sirali else 1

        no_w = 30
        kat_w = 140
        sag_w = 50
        bar_x = no_w + kat_w + 8
        bar_w = w - bar_x - sag_w - 8

        satir_y = 4

        for i, (kategori, sayi) in enumerate(sirali):
            # Sira no
            p.setPen(TEXT_FAINT)
            font = QFont("Inter", 14, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(0, satir_y, no_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, f"{i + 1}")

            # Kategori adi
            p.setPen(TEXT)
            font = QFont("Inter", 12, QFont.DemiBold)
            p.setFont(font)
            p.drawText(QRectF(no_w, satir_y, kat_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, kategori)

            # Bar arka plan
            p.setBrush(QColor("#f1f5f9"))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(QRectF(bar_x, satir_y + 11, bar_w, 10), 5, 5)

            # Bar dolu
            dolu_w = (sayi / max_v) * bar_w
            renk = PRIMARY if i == 0 else QColor("#94a3b8")
            p.setBrush(renk)
            p.drawRoundedRect(QRectF(bar_x, satir_y + 11, dolu_w, 10), 5, 5)

            # Sayi
            p.setPen(TEXT_DIM)
            font = QFont("Inter", 13, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(bar_x + bar_w + 8, satir_y, sag_w, 32),
                       Qt.AlignRight | Qt.AlignVCenter, str(sayi))

            satir_y += 40


# ─── AylikSatisGrafik ────────────────────────────────────

class AylikSatisGrafik(QWidget):
    """Modern dikey bar grafik - son 6 ay."""

    def __init__(self, veri: list = None, parent=None):
        super().__init__(parent)
        self.veri = veri or []
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def veri_ayarla(self, veri: list):
        self.veri = veri
        self.update()

    def paintEvent(self, e):
        if not self.veri:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        margin_sol = 20
        margin_sag = 20
        margin_ust = 20
        margin_alt = 40

        grafik_w = w - margin_sol - margin_sag
        grafik_h = h - margin_ust - margin_alt

        max_v = max(v for _, v in self.veri) if self.veri else 1
        if max_v == 0:
            max_v = 1

        n = len(self.veri)
        bar_genislik = min(48, grafik_w / n * 0.5)
        arasik = grafik_w / n

        for i, (ay, tutar) in enumerate(self.veri):
            bar_h = (tutar / max_v) * grafik_h if tutar > 0 else 2
            x = margin_sol + i * arasik + (arasik - bar_genislik) / 2
            y = margin_ust + grafik_h - bar_h

            # Son ay daha parlak
            if i == n - 1:
                renk = PRIMARY
            else:
                renk = QColor("#cbd5e1")

            p.setBrush(renk)
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(QRectF(x, y, bar_genislik, bar_h), 4, 4)

            # Ay etiketi
            p.setPen(TEXT_MUTED)
            font = QFont("Inter", 9, QFont.DemiBold)
            p.setFont(font)
            p.drawText(QRectF(x - 10, h - margin_alt + 8, bar_genislik + 20, 20),
                       Qt.AlignCenter, ay)

            # Tutar
            if tutar > 0:
                p.setPen(TEXT_DIM)
                font = QFont("Inter", 8, QFont.Bold)
                p.setFont(font)
                tutar_str = format_para(tutar).replace(" TL", "")
                p.drawText(QRectF(x - 20, y - 18, bar_genislik + 40, 16),
                           Qt.AlignCenter, tutar_str)

        # Alt cizgi
        p.setPen(QPen(BORDER, 1))
        p.drawLine(margin_sol, margin_ust + grafik_h,
                   w - margin_sag, margin_ust + grafik_h)


# ─── Kart ─────────────────────────────────────────────────

class Kart(QFrame):
    """Modern kart - yuvarlatilmis koseler, hafif golge."""

    def __init__(self, baslik: str = None, alt_baslik: str = None,
                 accent: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("Kart")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(12)

        if baslik:
            ust = QHBoxLayout()
            ust.setContentsMargins(0, 0, 0, 0)
            ust.setSpacing(0)

            if accent:
                marker = QFrame()
                marker.setFixedSize(3, 24)
                marker.setStyleSheet(
                    "background-color: #3b82f6; border: none; border-radius: 2px;"
                )
                ust.addWidget(marker, 0, Qt.AlignVCenter)
                ust.addSpacing(10)

            baslik_l = QVBoxLayout()
            baslik_l.setSpacing(2)
            baslik_l.setContentsMargins(0, 0, 0, 0)

            self.baslik_lbl = QLabel(baslik)
            self.baslik_lbl.setObjectName("KartBaslik")
            baslik_l.addWidget(self.baslik_lbl)

            if alt_baslik:
                self.alt_baslik_lbl = QLabel(alt_baslik)
                self.alt_baslik_lbl.setObjectName("KartAltBaslik")
                baslik_l.addWidget(self.alt_baslik_lbl)

            ust.addLayout(baslik_l)
            ust.addStretch()
            self.layout.addLayout(ust)

            ayrac = QFrame()
            ayrac.setObjectName("AyiriciInce")
            ayrac.setFixedHeight(1)
            ayrac.setStyleSheet("background-color: #f1f5f9;")
            self.layout.addWidget(ayrac)


# ─── Rozet ────────────────────────────────────────────────

class Rozet(QLabel):
    """Modern pill rozet - dolgu renkli arka plan."""

    STILLER = {
        "basari": (
            "background-color: #d1fae5; color: #065f46; "
            "border: none;"
        ),
        "uyari": (
            "background-color: #fef3c7; color: #92400e; "
            "border: none;"
        ),
        "tehlike": (
            "background-color: #fee2e2; color: #991b1b; "
            "border: none;"
        ),
        "notr": (
            "background-color: #f1f5f9; color: #64748b; "
            "border: none;"
        ),
    }

    def __init__(self, metin: str, tip: str = "basari", parent=None):
        super().__init__(metin, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(26)
        self.setMinimumWidth(80)

        renk_stil = self.STILLER.get(tip, self.STILLER["notr"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 4px; "
            f"padding: 4px 10px; "
            f"font-family: 'Inter', sans-serif; "
            f"font-size: 10px; font-weight: 700; }}"
        )


# ─── OncelikRozet ─────────────────────────────────────────

class OncelikRozet(QLabel):
    """Oncelik rozeti: yuksek=kirmizi, orta=amber, dusuk=yesil."""

    STILLER = {
        "yuksek": "background-color: #fee2e2; color: #991b1b; border: none;",
        "orta": "background-color: #fef3c7; color: #92400e; border: none;",
        "dusuk": "background-color: #d1fae5; color: #065f46; border: none;",
    }

    ETIKETLER = {"yuksek": "YUKSEK", "orta": "ORTA", "dusuk": "DUSUK"}

    def __init__(self, oncelik: str = "orta", parent=None):
        etiket = self.ETIKETLER.get(oncelik, "ORTA")
        super().__init__(etiket, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(26)
        self.setMinimumWidth(80)

        renk_stil = self.STILLER.get(oncelik, self.STILLER["orta"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 4px; padding: 4px 10px; "
            f"font-family: 'Inter', sans-serif; "
            f"font-size: 10px; font-weight: 700; }}"
        )


# ─── DurumRozeti ──────────────────────────────────────────

class DurumRozeti(QLabel):
    """Durum rozeti: ACIK=amber, CEVAPLANDI=yesil, KAPALI=gri."""

    STILLER = {
        "acik": "background-color: #fef3c7; color: #92400e; border: none;",
        "cevaplandi": "background-color: #d1fae5; color: #065f46; border: none;",
        "kapali": "background-color: #f1f5f9; color: #64748b; border: none;",
    }

    ETIKETLER = {"acik": "ACIK", "cevaplandi": "CEVAPLANDI", "kapali": "KAPALI"}

    def __init__(self, durum: str = "acik", parent=None):
        etiket = self.ETIKETLER.get(durum, "ACIK")
        super().__init__(etiket, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(26)
        self.setMinimumWidth(80)

        renk_stil = self.STILLER.get(durum, self.STILLER["acik"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 4px; padding: 4px 10px; "
            f"font-family: 'Inter', sans-serif; "
            f"font-size: 10px; font-weight: 700; }}"
        )


# ─── Yardimci sarmalacilar ────────────────────────────────

class HucreSarmalayici(QWidget):
    def __init__(self, icerik: QWidget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(0)
        layout.addWidget(icerik, 0, Qt.AlignVCenter)


class ButonGrubu(QWidget):
    def __init__(self, butonlar: list, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)
        for b in butonlar:
            layout.addWidget(b)
        layout.addStretch()


class Ayirici(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Ayirici")
        self.setFixedHeight(1)


class AyiriciInce(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AyiriciInce")
        self.setFixedHeight(1)
