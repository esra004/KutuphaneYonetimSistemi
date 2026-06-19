# models.py

class Kitap:
    # odunc_verilen parametresini varsayılan olarak 0 ayarladık, böylece hata vermeyecek
    def __init__(self, isbn, baslik, yazar, adet, odunc_verilen=0):
        self.isbn = isbn
        self.baslik = baslik
        self.yazar = yazar
        self.adet = adet
        self.odunc_verilen = odunc_verilen

    @property
    def musait_adet(self):
        return max(0, self.adet - self.odunc_verilen)


class Uye:
    def __init__(self, uye_id, isim, eposta, odunc_alinanlar=None):
        self.uye_id = uye_id
        self.isim = isim
        self.eposta = eposta
        self.odunc_alinanlar = odunc_alinanlar if odunc_alinanlar is not None else []