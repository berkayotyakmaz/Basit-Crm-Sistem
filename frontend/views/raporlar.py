"""
Raporlar sayfasi - En cok harcayan musteriler, aylik satis grafigi, urun dagilimi.
"""
import csv
import os
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Kart,
    MetrikKart,
    KategoriBarYatay,
    AylikSatisGrafik,
    format_para,
)


class RaporlarSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
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

        header = EditorialHeader(
            "RAPORLAR",
            "Raporlar",
            "Satis analizi, musteri siralama ve urun dagilimi.",
        )
        self.layout_ana.addWidget(header)

        # Metrik satir
        metrik_satir = QHBoxLayout()
        metrik_satir.setSpacing(16)

        self.kart_musteri = MetrikKart("Toplam Musteri")
        self.kart_ciro = MetrikKart("Toplam Ciro", accent=True)
        self.kart_talep_oran = MetrikKart("Acik Talep Orani")

        metrik_satir.addWidget(self.kart_musteri)
        metrik_satir.addWidget(self.kart_ciro)
        metrik_satir.addWidget(self.kart_talep_oran)
        self.layout_ana.addLayout(metrik_satir)

        # Iki kolon: grafik + top 5
        iki_kolon = QHBoxLayout()
        iki_kolon.setSpacing(16)

        # Aylik satis grafigi
        grafik_kart = Kart("Aylik Satis Grafigi", "Son 6 ay ciro dagilimi")
        self.grafik = AylikSatisGrafik()
        grafik_kart.layout.addWidget(self.grafik)
        iki_kolon.addWidget(grafik_kart, 1)

        # Top 5 musteri
        top_kart = Kart("En Cok Harcayan", "Top 5 musteri", accent=True)
        self.top_tablo = QTableWidget()
        self.top_tablo.setColumnCount(3)
        self.top_tablo.setHorizontalHeaderLabels(["#", "MUSTERI", "HARCAMA"])
        self.top_tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.top_tablo.setColumnWidth(0, 40)
        self.top_tablo.setColumnWidth(2, 140)
        self.top_tablo.verticalHeader().setVisible(False)
        self.top_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.top_tablo.setAlternatingRowColors(True)
        self.top_tablo.setMinimumHeight(250)
        top_kart.layout.addWidget(self.top_tablo)
        iki_kolon.addWidget(top_kart, 1)

        self.layout_ana.addLayout(iki_kolon)

        # Urun dagilimi
        urun_kart = Kart("Urun Dagilimi", "Satilan urunlerin adet bazli dagilimi")
        self.urun_bar = KategoriBarYatay({})
        urun_kart.layout.addWidget(self.urun_bar)
        self.layout_ana.addWidget(urun_kart)

        # CSV export
        export_btn = QPushButton("CSV OLARAK INDIR")
        export_btn.setObjectName("IkincilButon")
        export_btn.setFixedHeight(42)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self._csv_export)
        self.layout_ana.addWidget(export_btn)

        self.layout_ana.addStretch()

        scroll.setWidget(icerik)

        dis_layout = QVBoxLayout(self)
        dis_layout.setContentsMargins(0, 0, 0, 0)
        dis_layout.addWidget(scroll)

    def yenile(self):
        ist = self.vy.genel_istatistikler()

        self.kart_musteri.deger_ayarla(str(ist["toplam_musteri"]))
        self.kart_ciro.deger_ayarla(format_para(ist["toplam_ciro"]))

        toplam_talep = len(self.vy.tum_talepler())
        acik = ist["acik_talep"]
        oran = f"%{int(acik / toplam_talep * 100)}" if toplam_talep > 0 else "%0"
        self.kart_talep_oran.deger_ayarla(oran)
        self.kart_talep_oran.altyazi_ayarla(f"{acik}/{toplam_talep} talep acik")

        # Aylik grafik
        aylik = self.vy.aylik_ciro(6)
        self.grafik.veri_ayarla(aylik)

        # Top 5
        top = self.vy.en_cok_harcayan(5)
        self.top_tablo.setRowCount(len(top))
        for i, (m, tutar) in enumerate(top):
            sira = QTableWidgetItem(str(i + 1))
            sira.setTextAlignment(Qt.AlignCenter)
            self.top_tablo.setItem(i, 0, sira)
            self.top_tablo.setItem(i, 1, QTableWidgetItem(m.ad))
            tutar_item = QTableWidgetItem(format_para(tutar))
            tutar_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.top_tablo.setItem(i, 2, tutar_item)
            self.top_tablo.setRowHeight(i, 44)

        # Urun dagilimi
        dagilim = self.vy.urun_dagilimi()
        self.urun_bar.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.urun_bar.setMinimumHeight(n * 40 + 10)
        self.urun_bar.update()

    def _csv_export(self):
        dosya, _ = QFileDialog.getSaveFileName(
            self, "CSV Kaydet", "crm_rapor.csv", "CSV Dosyalari (*.csv)"
        )
        if not dosya:
            return

        try:
            with open(dosya, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Musteri", "Firma", "Telefon", "E-posta",
                                 "Toplam Harcama", "Acik Talep"])
                for m in self.vy.tum_musteriler():
                    harcama = self.vy.musteri_toplam_harcama(m.musteri_id)
                    acik = self.vy.musteri_acik_talep_sayisi(m.musteri_id)
                    writer.writerow([
                        m.ad, m.firma, m.telefon, m.email,
                        f"{harcama:.2f}", acik
                    ])
            QMessageBox.information(self, "Basarili", f"Rapor kaydedildi:\n{dosya}")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Dosya kaydedilemedi:\n{e}")
