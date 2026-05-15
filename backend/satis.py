"""
Satis sinifi - Satis kayitlari veri modeli.
"""
from datetime import datetime


class Satis:
    def __init__(
        self,
        satis_id: int,
        musteri_id: int,
        urun: str,
        fiyat: float,
        adet: int = 1,
        tarih: str = None,
    ):
        self.satis_id = satis_id
        self.musteri_id = musteri_id
        self.urun = urun.strip()
        self.fiyat = float(fiyat)
        self.adet = int(adet)
        self.tarih = tarih or datetime.now().strftime("%d.%m.%Y")

    def toplam_tutar(self) -> float:
        return self.fiyat * self.adet

    def to_dict(self) -> dict:
        return {
            "satis_id": self.satis_id,
            "musteri_id": self.musteri_id,
            "urun": self.urun,
            "fiyat": self.fiyat,
            "adet": self.adet,
            "tarih": self.tarih,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Satis":
        return cls(**d)
