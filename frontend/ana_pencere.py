"""
Ana Pencere - Modern corporate koyu sidebar + 6 sayfa stack.
"""
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QButtonGroup,
    QFrame,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi
from frontend.tema import ANA_STIL
from frontend.widgets.bilesenler import Masthead, MuhurAvatar
from frontend.views.dashboard import DashboardSayfasi
from frontend.views.musteriler import MusterilerSayfasi
from frontend.views.musteri_detay import MusteriDetaySayfasi
from frontend.views.satislar import SatislarSayfasi
from frontend.views.talepler import TaleplerSayfasi
from frontend.views.raporlar import RaporlarSayfasi


class AnaPencere(QMainWindow):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None):
        super().__init__()
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici

        self.setWindowTitle("Musteri Defteri - CRM Sistemi")
        self.setMinimumSize(1180, 760)
        self.resize(1380, 880)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        merkez = QWidget()
        ana = QHBoxLayout(merkez)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        sidebar = self._sidebar_olustur()
        ana.addWidget(sidebar)

        icerik_sarici = QWidget()
        icerik_sarici.setStyleSheet("background-color: #fdfdfb;")
        icerik_layout = QVBoxLayout(icerik_sarici)
        icerik_layout.setContentsMargins(0, 0, 0, 0)
        icerik_layout.setSpacing(0)

        self.yigin = QStackedWidget()

        self.sayfa_dashboard = DashboardSayfasi(self.vy, self.aktif_kullanici)
        self.sayfa_musteriler = MusterilerSayfasi(self.vy)
        self.sayfa_musteri_detay = MusteriDetaySayfasi(self.vy)
        self.sayfa_satislar = SatislarSayfasi(self.vy)
        self.sayfa_talepler = TaleplerSayfasi(self.vy)
        self.sayfa_raporlar = RaporlarSayfasi(self.vy)

        self.sayfa_musteriler.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_satislar.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_talepler.veri_degisti.connect(self._tumunu_yenile)

        # Musteri detay navigasyonu
        self.sayfa_musteriler.musteri_secildi.connect(self._musteri_detay_goster)
        self.sayfa_musteri_detay.geri_signal.connect(self._musteri_listesine_don)

        self.yigin.addWidget(self.sayfa_dashboard)       # 0
        self.yigin.addWidget(self.sayfa_musteriler)       # 1
        self.yigin.addWidget(self.sayfa_musteri_detay)    # 2
        self.yigin.addWidget(self.sayfa_satislar)         # 3
        self.yigin.addWidget(self.sayfa_talepler)         # 4
        self.yigin.addWidget(self.sayfa_raporlar)         # 5

        icerik_layout.addWidget(self.yigin)
        ana.addWidget(icerik_sarici, 1)

        self.setCentralWidget(merkez)
        self.yigin.setCurrentIndex(0)

    def _sidebar_olustur(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(264)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        layout.addWidget(Masthead())
        layout.addSpacing(28)

        layout.addWidget(self._menu_baslik("MENU"))

        self.buton_grubu = QButtonGroup(self)
        self.buton_grubu.setExclusive(True)

        self._menu_butonu_ekle(layout, "Dashboard", 0)
        self._menu_butonu_ekle(layout, "Musteriler", 1)
        self._menu_butonu_ekle(layout, "Satislar", 3)
        self._menu_butonu_ekle(layout, "Destek Talepleri", 4)
        self._menu_butonu_ekle(layout, "Raporlar", 5)

        self.buton_grubu.button(0).setChecked(True)

        layout.addStretch()

        # Kullanici karti
        kart_sarici = QHBoxLayout()
        kart_sarici.setContentsMargins(16, 0, 16, 0)

        kullanici_kart = QFrame()
        kullanici_kart.setObjectName("KullaniciKart")

        kk_layout = QHBoxLayout(kullanici_kart)
        kk_layout.setContentsMargins(14, 14, 14, 14)
        kk_layout.setSpacing(12)

        if self.aktif_kullanici:
            ad_str = self.aktif_kullanici.ad
            rol_str = self.aktif_kullanici.rol.upper()
        else:
            ad_str = "Kullanici"
            rol_str = "MISAFIR"

        avatar = MuhurAvatar(ad_str, boyut=40)

        kullanici_bilgi = QVBoxLayout()
        kullanici_bilgi.setSpacing(2)
        kullanici_bilgi.setContentsMargins(0, 0, 0, 0)

        ust_satir = QHBoxLayout()
        ust_satir.setSpacing(8)
        ust_satir.setContentsMargins(0, 0, 0, 0)

        ad = QLabel(ad_str)
        ad.setObjectName("KullaniciAd")

        plan = QLabel("EDITOR")
        plan.setObjectName("PlanRozet")
        plan.setAlignment(Qt.AlignCenter)
        plan.setMinimumWidth(54)
        plan.setMinimumHeight(20)

        ust_satir.addWidget(ad)
        ust_satir.addWidget(plan)
        ust_satir.addStretch()

        durum = QLabel(rol_str)
        durum.setObjectName("KullaniciDurum")

        kullanici_bilgi.addLayout(ust_satir)
        kullanici_bilgi.addWidget(durum)

        kk_layout.addWidget(avatar)
        kk_layout.addLayout(kullanici_bilgi)
        kk_layout.addStretch()

        cikis_btn = QPushButton("X")
        cikis_btn.setFixedSize(30, 30)
        cikis_btn.setCursor(Qt.PointingHandCursor)
        cikis_btn.setToolTip("Cikis yap")
        cikis_btn.setStyleSheet(
            "QPushButton { background-color: transparent; "
            "color: #94a3b8; border: 1px solid rgba(255,255,255,0.15); "
            "border-radius: 6px; font-size: 14px; padding: 0; "
            "letter-spacing: 0; } "
            "QPushButton:hover { color: #ffffff; "
            "background-color: #ef4444; "
            "border: 1px solid #ef4444; }"
        )
        cikis_btn.clicked.connect(self._cikis_yap)
        kk_layout.addWidget(cikis_btn, 0, Qt.AlignVCenter)

        kart_sarici.addWidget(kullanici_kart)
        layout.addLayout(kart_sarici)

        return sidebar

    def _menu_baslik(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setObjectName("MenuBaslik")
        lbl.setContentsMargins(24, 0, 24, 10)
        return lbl

    def _menu_butonu_ekle(self, layout, metin: str, indeks: int):
        btn = QPushButton(metin)
        btn.setObjectName("MenuButon")
        btn.setCheckable(True)
        btn.setFixedHeight(38)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda _, i=indeks: self._sayfa_degistir(i))
        self.buton_grubu.addButton(btn, indeks)
        layout.addWidget(btn)

    def _cikis_yap(self):
        from PyQt5.QtWidgets import QMessageBox
        cevap = QMessageBox.question(
            self, "Oturum Sonlandir",
            "Oturumu kapatip giris ekranina donmek istediginize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()

    def _sayfa_degistir(self, indeks: int):
        self.yigin.setCurrentIndex(indeks)
        sayfa = self.yigin.widget(indeks)
        if hasattr(sayfa, "yenile"):
            sayfa.yenile()

    def _musteri_detay_goster(self, musteri_id: int):
        self.sayfa_musteri_detay.musteri_goster(musteri_id)
        self.yigin.setCurrentIndex(2)

    def _musteri_listesine_don(self):
        self.yigin.setCurrentIndex(1)
        self.sayfa_musteriler.yenile()

    def _tumunu_yenile(self):
        for i in range(self.yigin.count()):
            sayfa = self.yigin.widget(i)
            if hasattr(sayfa, "yenile"):
                sayfa.yenile()
