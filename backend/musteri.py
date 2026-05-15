"""
Musteri sinifi - CRM sistemi temel veri modeli.
"""
from datetime import datetime


class Musteri:
    def __init__(
        self,
        musteri_id: int,
        ad: str,
        telefon: str,
        email: str = "",
        firma: str = "",
        kayit_tarihi: str = None,
    ):
        self.musteri_id = musteri_id
        self.ad = ad.strip()
        self.telefon = self._temizle_telefon(telefon)
        self.email = email.strip()
        self.firma = firma.strip()
        self.kayit_tarihi = kayit_tarihi or datetime.now().strftime("%d.%m.%Y")

    @staticmethod
    def _temizle_telefon(telefon: str) -> str:
        return "".join(c for c in telefon if c.isdigit())

    def toplam_harcama(self, satislar: list) -> float:
        return sum(s.toplam_tutar() for s in satislar if s.musteri_id == self.musteri_id)

    def acik_talepler(self, talepler: list) -> list:
        return [t for t in talepler if t.musteri_id == self.musteri_id and t.acik_mi()]

    def to_dict(self) -> dict:
        return {
            "musteri_id": self.musteri_id,
            "ad": self.ad,
            "telefon": self.telefon,
            "email": self.email,
            "firma": self.firma,
            "kayit_tarihi": self.kayit_tarihi,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Musteri":
        return cls(**d)
