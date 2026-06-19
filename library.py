# library.py
import json
import os
from models import Kitap, Uye

class Kutuphane:
    def __init__(self, dosya_adi="kutuphane_verileri.json"):
        self.dosya_adi = dosya_adi
        self.kitaplar = {}
        self.uyeler = {}
        self.verileri_yukle()

    def kitap_bagis_al(self, isbn, baslik, yazar, adet):
        if isbn in self.kitaplar:
            self.kitaplar[isbn].adet += adet
        else:
            self.kitaplar[isbn] = Kitap(isbn, baslik, yazar, adet)
        self.verileri_kaydet()

    def uye_ekle(self, uye_id, isim, eposta):
        if uye_id not in self.uyeler:
            self.uyeler[uye_id] = Uye(uye_id, isim, eposta)
            self.verileri_kaydet()

    def kitap_odunc_ver(self, uye_id, isbn):
        if uye_id in self.uyeler and isbn in self.kitaplar:
            uye = self.uyeler[uye_id]
            kitap = self.kitaplar[isbn]
            
            if isbn not in uye.odunc_alinanlar and kitap.musait_adet > 0:
                uye.odunc_alinanlar.append(isbn)
                kitap.odunc_verilen += 1
                self.verileri_kaydet()
                return True
        return False

    def kitap_iade_al(self, uye_id, isbn):
        if uye_id in self.uyeler and isbn in self.kitaplar:
            uye = self.uyeler[uye_id]
            kitap = self.kitaplar[isbn]
            
            if isbn in uye.odunc_alinanlar:
                uye.odunc_alinanlar.remove(isbn)
                kitap.odunc_verilen = max(0, kitap.odunc_verilen - 1)
                self.verileri_kaydet()
                return True
        return False

    def verileri_kaydet(self):
        """Tüm kitap ve üyeleri JSON dosyasına kalıcı olarak kaydeder."""
        try:
            veri = {
                "kitaplar": {
                    isbn: {
                        "isbn": k.isbn, "baslik": k.baslik, "yazar": k.yazar, 
                        "adet": k.adet, "odunc_verilen": k.odunc_verilen
                    } for isbn, k in self.kitaplar.items()
                },
                "uyeler": {
                    uye_id: {
                        "uye_id": u.uye_id, "isim": u.isim, "eposta": u.eposta, 
                        "odunc_alinanlar": u.odunc_alinanlar
                    } for uye_id, u in self.uyeler.items()
                }
            }
            with open(self.dosya_adi, "w", encoding="utf-8") as f:
                json.dump(veri, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Veriler diske yazılırken bir hata oluştu: {e}")

    def verileri_yukle(self):
        """Program açılırken kayıtlı JSON verilerini nesnelere dönüştürerek yükler."""
        if not os.path.exists(self.dosya_adi):
            return
        try:
            with open(self.dosya_adi, "r", encoding="utf-8") as f:
                veri = json.load(f)
                
                # Kitapları yükle
                for isbn, k_veri in veri.get("kitaplar", {}).items():
                    self.kitaplar[isbn] = Kitap(
                        isbn=k_veri["isbn"], baslik=k_veri["baslik"], yazar=k_veri["yazar"],
                        adet=k_veri["adet"], odunc_verilen=k_veri["odunc_verilen"]
                    )
                
                # Üyeleri yükle
                for uye_id, u_veri in veri.get("uyeler", {}).items():
                    self.uyeler[uye_id] = Uye(
                        uye_id=u_veri["uye_id"], isim=u_veri["isim"], eposta=u_veri["eposta"],
                        odunc_alinanlar=u_veri["odunc_alinanlar"]
                    )
        except Exception as e:
            print(f"Veriler yüklenirken hata oluştu: {e}")