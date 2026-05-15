"""
VeriYoneticisi - JSON tabanli CRUD + is mantigi.
"""
import json
import os
from datetime import datetime, timedelta

from backend.musteri import Musteri
from backend.satis import Satis
from backend.destek_talebi import DestekTalebi


class VeriYoneticisi:
    def __init__(self, veri_klasoru: str = "data"):
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self._musteri_dosya = os.path.join(veri_klasoru, "musteriler.json")
        self._satis_dosya = os.path.join(veri_klasoru, "satislar.json")
        self._talep_dosya = os.path.join(veri_klasoru, "talepler.json")

        self._musteriler: list[Musteri] = []
        self._satislar: list[Satis] = []
        self._talepler: list[DestekTalebi] = []

        self._yukle()

    # ─── Kalicilik ───────────────────────────────────────

    def _yukle(self):
        self._musteriler = self._dosya_oku(self._musteri_dosya, Musteri)
        self._satislar = self._dosya_oku(self._satis_dosya, Satis)
        self._talepler = self._dosya_oku(self._talep_dosya, DestekTalebi)

    @staticmethod
    def _dosya_oku(dosya: str, sinif):
        if not os.path.exists(dosya):
            return []
        try:
            with open(dosya, "r", encoding="utf-8") as f:
                veri = json.load(f)
                return [sinif.from_dict(d) for d in veri]
        except (json.JSONDecodeError, KeyError, TypeError):
            return []

    def _kaydet_musteriler(self):
        self._dosya_yaz(self._musteri_dosya, self._musteriler)

    def _kaydet_satislar(self):
        self._dosya_yaz(self._satis_dosya, self._satislar)

    def _kaydet_talepler(self):
        self._dosya_yaz(self._talep_dosya, self._talepler)

    @staticmethod
    def _dosya_yaz(dosya: str, liste: list):
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in liste], f, ensure_ascii=False, indent=2)

    # ─── Musteri CRUD ────────────────────────────────────

    def tum_musteriler(self) -> list[Musteri]:
        return list(self._musteriler)

    def musteri_bul(self, musteri_id: int) -> Musteri | None:
        for m in self._musteriler:
            if m.musteri_id == musteri_id:
                return m
        return None

    def _sonraki_musteri_id(self) -> int:
        if not self._musteriler:
            return 1
        return max(m.musteri_id for m in self._musteriler) + 1

    def musteri_ekle(self, ad: str, telefon: str, email: str = "",
                     firma: str = "") -> Musteri:
        telefon_temiz = "".join(c for c in telefon if c.isdigit())
        if not ad.strip():
            raise ValueError("Musteri adi bos olamaz.")
        if len(telefon_temiz) < 10 or len(telefon_temiz) > 11:
            raise ValueError("Telefon numarasi 10-11 haneli olmali.")
        for m in self._musteriler:
            if m.telefon == telefon_temiz:
                raise ValueError("Bu telefon numarasi zaten kayitli.")

        yeni = Musteri(
            musteri_id=self._sonraki_musteri_id(),
            ad=ad,
            telefon=telefon_temiz,
            email=email,
            firma=firma,
        )
        self._musteriler.append(yeni)
        self._kaydet_musteriler()
        return yeni

    def musteri_guncelle(self, musteri_id: int, ad: str, telefon: str,
                         email: str = "", firma: str = ""):
        m = self.musteri_bul(musteri_id)
        if not m:
            raise ValueError("Musteri bulunamadi.")
        telefon_temiz = "".join(c for c in telefon if c.isdigit())
        if len(telefon_temiz) < 10 or len(telefon_temiz) > 11:
            raise ValueError("Telefon numarasi 10-11 haneli olmali.")
        for diger in self._musteriler:
            if diger.telefon == telefon_temiz and diger.musteri_id != musteri_id:
                raise ValueError("Bu telefon numarasi zaten kayitli.")
        m.ad = ad.strip()
        m.telefon = telefon_temiz
        m.email = email.strip()
        m.firma = firma.strip()
        self._kaydet_musteriler()

    def musteri_sil(self, musteri_id: int):
        m = self.musteri_bul(musteri_id)
        if not m:
            raise ValueError("Musteri bulunamadi.")
        ilgili_satis = [s for s in self._satislar if s.musteri_id == musteri_id]
        ilgili_talep = [t for t in self._talepler if t.musteri_id == musteri_id]
        if ilgili_satis or ilgili_talep:
            raise ValueError(
                "Bu musteriye ait satis veya destek talebi var. "
                "Once bunlari silmelisiniz."
            )
        self._musteriler.remove(m)
        self._kaydet_musteriler()

    # ─── Satis CRUD ──────────────────────────────────────

    def tum_satislar(self) -> list[Satis]:
        return list(self._satislar)

    def satis_bul(self, satis_id: int) -> Satis | None:
        for s in self._satislar:
            if s.satis_id == satis_id:
                return s
        return None

    def _sonraki_satis_id(self) -> int:
        if not self._satislar:
            return 1
        return max(s.satis_id for s in self._satislar) + 1

    def satis_ekle(self, musteri_id: int, urun: str, fiyat: float,
                   adet: int = 1, tarih: str = None) -> Satis:
        if not self.musteri_bul(musteri_id):
            raise ValueError("Musteri bulunamadi.")
        if not urun.strip():
            raise ValueError("Urun adi bos olamaz.")
        if fiyat <= 0:
            raise ValueError("Fiyat 0'dan buyuk olmali.")
        if adet < 1:
            raise ValueError("Adet en az 1 olmali.")

        yeni = Satis(
            satis_id=self._sonraki_satis_id(),
            musteri_id=musteri_id,
            urun=urun,
            fiyat=fiyat,
            adet=adet,
            tarih=tarih,
        )
        self._satislar.append(yeni)
        self._kaydet_satislar()
        return yeni

    def satis_sil(self, satis_id: int):
        s = self.satis_bul(satis_id)
        if not s:
            raise ValueError("Satis bulunamadi.")
        self._satislar.remove(s)
        self._kaydet_satislar()

    # ─── Talep CRUD ──────────────────────────────────────

    def tum_talepler(self) -> list[DestekTalebi]:
        return list(self._talepler)

    def talep_bul(self, talep_id: int) -> DestekTalebi | None:
        for t in self._talepler:
            if t.talep_id == talep_id:
                return t
        return None

    def _sonraki_talep_id(self) -> int:
        if not self._talepler:
            return 1
        return max(t.talep_id for t in self._talepler) + 1

    def talep_ekle(self, musteri_id: int, aciklama: str,
                   oncelik: str = "orta") -> DestekTalebi:
        if not self.musteri_bul(musteri_id):
            raise ValueError("Musteri bulunamadi.")
        if not aciklama.strip():
            raise ValueError("Aciklama bos olamaz.")
        if oncelik not in ("dusuk", "orta", "yuksek"):
            raise ValueError("Oncelik dusuk/orta/yuksek olmali.")

        yeni = DestekTalebi(
            talep_id=self._sonraki_talep_id(),
            musteri_id=musteri_id,
            aciklama=aciklama,
            oncelik=oncelik,
        )
        self._talepler.append(yeni)
        self._kaydet_talepler()
        return yeni

    def talep_cevapla(self, talep_id: int):
        t = self.talep_bul(talep_id)
        if not t:
            raise ValueError("Talep bulunamadi.")
        t.cevapla()
        self._kaydet_talepler()

    def talep_kapat(self, talep_id: int):
        t = self.talep_bul(talep_id)
        if not t:
            raise ValueError("Talep bulunamadi.")
        t.kapat()
        self._kaydet_talepler()

    def talep_sil(self, talep_id: int):
        t = self.talep_bul(talep_id)
        if not t:
            raise ValueError("Talep bulunamadi.")
        self._talepler.remove(t)
        self._kaydet_talepler()

    # ─── Istatistikler ───────────────────────────────────

    def toplam_ciro(self) -> float:
        return sum(s.toplam_tutar() for s in self._satislar)

    def acik_talep_sayisi(self) -> int:
        return sum(1 for t in self._talepler if t.acik_mi())

    def musteri_toplam_harcama(self, musteri_id: int) -> float:
        return sum(s.toplam_tutar() for s in self._satislar if s.musteri_id == musteri_id)

    def musteri_acik_talep_sayisi(self, musteri_id: int) -> int:
        return sum(1 for t in self._talepler
                   if t.musteri_id == musteri_id and t.acik_mi())

    def acil_talepler(self, limit: int = 5) -> list[DestekTalebi]:
        acil = [t for t in self._talepler
                if t.oncelik == "yuksek" and t.acik_mi()]
        return acil[:limit]

    def son_satislar(self, limit: int = 5) -> list[Satis]:
        sirali = sorted(self._satislar, key=lambda s: s.satis_id, reverse=True)
        return sirali[:limit]

    def en_cok_harcayan(self, limit: int = 5) -> list[tuple]:
        harcama = {}
        for s in self._satislar:
            harcama[s.musteri_id] = harcama.get(s.musteri_id, 0) + s.toplam_tutar()
        sirali = sorted(harcama.items(), key=lambda x: -x[1])
        sonuc = []
        for mid, tutar in sirali[:limit]:
            m = self.musteri_bul(mid)
            if m:
                sonuc.append((m, tutar))
        return sonuc

    def aylik_ciro(self, ay_sayisi: int = 6) -> list[tuple]:
        bugun = datetime.now()
        sonuc = []
        for i in range(ay_sayisi - 1, -1, -1):
            ay_tarihi = bugun - timedelta(days=i * 30)
            ay = ay_tarihi.month
            yil = ay_tarihi.year
            toplam = 0
            for s in self._satislar:
                try:
                    t = datetime.strptime(s.tarih, "%d.%m.%Y")
                    if t.month == ay and t.year == yil:
                        toplam += s.toplam_tutar()
                except ValueError:
                    pass
            ay_isimleri = ["", "OCA", "SUB", "MAR", "NIS", "MAY", "HAZ",
                           "TEM", "AGU", "EYL", "EKI", "KAS", "ARA"]
            sonuc.append((ay_isimleri[ay], toplam))
        return sonuc

    def urun_dagilimi(self) -> dict:
        dagilim = {}
        for s in self._satislar:
            dagilim[s.urun] = dagilim.get(s.urun, 0) + s.adet
        return dagilim

    def genel_istatistikler(self) -> dict:
        return {
            "toplam_musteri": len(self._musteriler),
            "toplam_satis": len(self._satislar),
            "toplam_ciro": self.toplam_ciro(),
            "acik_talep": self.acik_talep_sayisi(),
        }
