"""
Kullanici sinifi - Login icin basit kullanici modeli.
"""


class Kullanici:
    def __init__(self, kullanici_id: int, ad: str):
        self.kullanici_id = kullanici_id
        self.ad = ad

    def to_dict(self) -> dict:
        return {"kullanici_id": self.kullanici_id, "ad": self.ad}

    @classmethod
    def from_dict(cls, d: dict) -> "Kullanici":
        return cls(**d)
