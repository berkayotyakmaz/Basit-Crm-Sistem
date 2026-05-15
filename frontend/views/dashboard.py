"""
Dashboard sayfasi - Metrik kartlar + acil talepler + son satislar.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea,
    QFrame,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    ManseteKart,
    MetrikKart,
    Kart,
    Rozet,
    OncelikRozet,
    DurumRozeti,
    HucreSarmalayici,
    format_para,
    format_telefon,
)


class DashboardSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        icerik = QWidget()
        self.layout_ana = QVBoxLayout(icerik)
        self.layout_ana.setContentsMargins(40, 32, 40, 32)
        self.layout_ana.setSpacing(24)

        # Manset
        ad = self.aktif_kullanici.ad if self.aktif_kullanici else "Kullanici"
        self.manset = ManseteKart(
            baslik="Hos Geldin, " + ad,
            altyazi="Musterilerini, satislarini ve destek taleplerini tek panelden yonet.",
            by_line="MUSTERI DEFTERI · CRM SISTEMI",
        )
        self.layout_ana.addWidget(self.manset)

        # 4 Metrik kart
        metrik_satir = QHBoxLayout()
        metrik_satir.setSpacing(16)

        self.kart_musteri = MetrikKart("Toplam Musteri", accent=True)
        self.kart_satis = MetrikKart("Toplam Satis")
        self.kart_ciro = MetrikKart("Toplam Ciro")
        self.kart_talep = MetrikKart("Acik Talep", accent=True)

        metrik_satir.addWidget(self.kart_musteri)
        metrik_satir.addWidget(self.kart_satis)
        metrik_satir.addWidget(self.kart_ciro)
        metrik_satir.addWidget(self.kart_talep)
        self.layout_ana.addLayout(metrik_satir)

        # Alt bolum: Acil talepler + Son satislar
        alt = QHBoxLayout()
        alt.setSpacing(16)

        # Acil talepler
        acil_kart = Kart("Acil Talepler", "Yuksek oncelikli acik talepler", accent=True)
        self.acil_tablo = QTableWidget()
        self.acil_tablo.setColumnCount(4)
        self.acil_tablo.setHorizontalHeaderLabels(["MUSTERI", "ACIKLAMA", "DURUM", "ONCELIK"])
        self.acil_tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.acil_tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.acil_tablo.verticalHeader().setVisible(False)
        self.acil_tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.acil_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.acil_tablo.setAlternatingRowColors(True)
        self.acil_tablo.setMinimumHeight(200)
        acil_kart.layout.addWidget(self.acil_tablo)
        alt.addWidget(acil_kart, 1)

        # Son satislar
        son_kart = Kart("Son Satislar", "En son yapilan satislar")
        self.son_tablo = QTableWidget()
        self.son_tablo.setColumnCount(4)
        self.son_tablo.setHorizontalHeaderLabels(["MUSTERI", "URUN", "TUTAR", "TARIH"])
        self.son_tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.son_tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.son_tablo.verticalHeader().setVisible(False)
        self.son_tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.son_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.son_tablo.setAlternatingRowColors(True)
        self.son_tablo.setMinimumHeight(200)
        son_kart.layout.addWidget(self.son_tablo)
        alt.addWidget(son_kart, 1)

        self.layout_ana.addLayout(alt)
        self.layout_ana.addStretch()

        scroll.setWidget(icerik)

        dis_layout = QVBoxLayout(self)
        dis_layout.setContentsMargins(0, 0, 0, 0)
        dis_layout.addWidget(scroll)

    def yenile(self):
        ist = self.vy.genel_istatistikler()

        self.kart_musteri.deger_ayarla(str(ist["toplam_musteri"]))
        self.kart_satis.deger_ayarla(str(ist["toplam_satis"]))
        self.kart_ciro.deger_ayarla(format_para(ist["toplam_ciro"]))
        self.kart_talep.deger_ayarla(str(ist["acik_talep"]))

        self.manset.metrikleri_ayarla([
            ("Musteri", str(ist["toplam_musteri"])),
            ("Satis", str(ist["toplam_satis"])),
            ("Ciro", format_para(ist["toplam_ciro"])),
            ("Acik Talep", str(ist["acik_talep"])),
        ])

        # Acil talepler
        acil = self.vy.acil_talepler(5)
        self.acil_tablo.setRowCount(len(acil))
        for i, t in enumerate(acil):
            m = self.vy.musteri_bul(t.musteri_id)
            self.acil_tablo.setItem(i, 0, QTableWidgetItem(m.ad if m else "?"))
            self.acil_tablo.setItem(i, 1, QTableWidgetItem(t.aciklama[:60]))
            self.acil_tablo.setCellWidget(i, 2, HucreSarmalayici(DurumRozeti(t.durum)))
            self.acil_tablo.setCellWidget(i, 3, HucreSarmalayici(OncelikRozet(t.oncelik)))
            self.acil_tablo.setRowHeight(i, 48)

        # Son satislar
        son = self.vy.son_satislar(5)
        self.son_tablo.setRowCount(len(son))
        for i, s in enumerate(son):
            m = self.vy.musteri_bul(s.musteri_id)
            self.son_tablo.setItem(i, 0, QTableWidgetItem(m.ad if m else "?"))
            self.son_tablo.setItem(i, 1, QTableWidgetItem(s.urun))

            tutar_item = QTableWidgetItem(format_para(s.toplam_tutar()))
            tutar_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.son_tablo.setItem(i, 2, tutar_item)

            self.son_tablo.setItem(i, 3, QTableWidgetItem(s.tarih))
            self.son_tablo.setRowHeight(i, 48)
