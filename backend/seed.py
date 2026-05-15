"""
Seed verisi - 12 musteri, 25 satis, 8 destek talebi.
"""
from datetime import datetime, timedelta
import random


def seed_gerekli_mi(vy) -> bool:
    return len(vy.tum_musteriler()) == 0


def seed_uygula(vy):
    random.seed(42)
    bugun = datetime.now()

    # ─── Musteriler (12) ─────────────────────────────────
    musteriler_veri = [
        ("Beko Yilmaz", "05321234567", "beko@mail.com", ""),
        ("Ahmet Demir", "02125551234", "ahmet@anyotekstil.com", "Anyo Tekstil A.S."),
        ("Selim Kaya", "05331112233", "selim@mail.com", ""),
        ("Zeynep Celik", "02164445678", "zeynep@maviyazilim.com", "Mavi Yazilim Ltd."),
        ("Ali Sahin", "05442223344", "ali@mail.com", ""),
        ("Ayse Yilmaz", "03123331122", "ayse@cicekbotanik.com", "Cicek Botanik"),
        ("Murat Aydin", "05553334455", "murat@mail.com", ""),
        ("Can Ozturk", "02322223344", "can@starkafe.com", "Star Kafe"),
        ("Selin Yildiz", "05364445566", "selin@mail.com", ""),
        ("Mehmet Koc", "02246667788", "mehmet@kuzeyinsaat.com", "Kuzey Insaat"),
        ("Pinar Dogan", "05425556677", "pinar@mail.com", ""),
        ("Tolga Erdem", "02425556677", "tolga@laleeczanesi.com", "Lale Eczanesi"),
    ]
    for ad, tel, email, firma in musteriler_veri:
        vy.musteri_ekle(ad=ad, telefon=tel, email=email, firma=firma)

    # ─── Satislar (25) ───────────────────────────────────
    urunler = [
        ("Premium Yazilim Lisansi", 15000),
        ("Aylik Abonelik", 1500),
        ("Web Tasarimi", 25000),
        ("SEO Paketi", 8000),
        ("Hosting (1 Yil)", 2500),
        ("Domain", 500),
        ("Logo Tasarimi", 5000),
        ("Sosyal Medya Yonetimi", 12000),
    ]

    satislar_veri = [
        (1, 0, 2), (1, 2, 1), (2, 3, 1), (2, 1, 3),
        (3, 4, 1), (4, 0, 1), (4, 7, 1), (5, 5, 2),
        (5, 1, 1), (6, 6, 1), (6, 2, 1), (7, 0, 1),
        (7, 3, 1), (8, 4, 1), (8, 7, 2), (9, 1, 1),
        (9, 5, 1), (10, 0, 1), (10, 6, 1), (11, 2, 1),
        (11, 3, 1), (12, 7, 1), (12, 4, 1), (1, 7, 1),
        (3, 0, 1),
    ]

    for musteri_id, urun_idx, adet in satislar_veri:
        urun, fiyat = urunler[urun_idx]
        gun_once = random.randint(1, 180)
        tarih = (bugun - timedelta(days=gun_once)).strftime("%d.%m.%Y")
        vy.satis_ekle(
            musteri_id=musteri_id,
            urun=urun,
            fiyat=fiyat,
            adet=adet,
            tarih=tarih,
        )

    # ─── Destek Talepleri (8) ────────────────────────────
    talepler_veri = [
        (1, "Faturami bulamiyorum, yardim eder misiniz?", "yuksek", "acik"),
        (2, "Yazilim acilmiyor lutfen yardim", "yuksek", "acik"),
        (4, "Iade istiyorum, urun tarif edilen gibi degil", "yuksek", "acik"),
        (3, "Hosting yavasliyor, performans sorunu var", "orta", "cevaplandi"),
        (6, "Logo dosyasini tekrar gonderir misiniz?", "dusuk", "cevaplandi"),
        (5, "SEO raporunu ne zaman alirim?", "orta", "kapali"),
        (8, "Domain yonlendirmesi calismiyor", "orta", "kapali"),
        (10, "Abonelik iptali hakkinda bilgi istiyorum", "dusuk", "kapali"),
    ]

    for musteri_id, aciklama, oncelik, durum in talepler_veri:
        t = vy.talep_ekle(
            musteri_id=musteri_id,
            aciklama=aciklama,
            oncelik=oncelik,
        )
        if durum == "cevaplandi":
            vy.talep_cevapla(t.talep_id)
        elif durum == "kapali":
            vy.talep_cevapla(t.talep_id)
            vy.talep_kapat(t.talep_id)
