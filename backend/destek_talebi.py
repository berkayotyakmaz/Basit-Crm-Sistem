"""
DestekTalebi sinifi - Destek talepleri veri modeli.
"""
from datetime import datetime


class DestekTalebi:
    def __init__(
        self,
        talep_id: int,
        musteri_id: int,
        aciklama: str,
        durum: str = "acik",
        oncelik: str = "orta",
        olusturma_tarihi: str = None,
        kapanis_tarihi: str = None,
    ):
        self.talep_id = talep_id
        self.musteri_id = musteri_id
        self.aciklama = aciklama.strip()
        self.durum = durum
        self.oncelik = oncelik
        self.olusturma_tarihi = olusturma_tarihi or datetime.now().strftime("%d.%m.%Y")
        self.kapanis_tarihi = kapanis_tarihi

    def cevapla(self, yanit: str = ""):
        self.durum = "cevaplandi"

    def kapat(self):
        self.durum = "kapali"
        self.kapanis_tarihi = datetime.now().strftime("%d.%m.%Y")

    def acik_mi(self) -> bool:
        return self.durum != "kapali"

    def to_dict(self) -> dict:
        return {
            "talep_id": self.talep_id,
            "musteri_id": self.musteri_id,
            "aciklama": self.aciklama,
            "durum": self.durum,
            "oncelik": self.oncelik,
            "olusturma_tarihi": self.olusturma_tarihi,
            "kapanis_tarihi": self.kapanis_tarihi,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DestekTalebi":
        return cls(**d)
