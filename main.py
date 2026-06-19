# main.py
import tkinter as tk
from tkinter import messagebox, ttk
from library import Kutuphane

class KutuphaneArayuz:
    def __init__(self, root):
        self.root = root
        self.root.title(" ✨ Orion Kütüphanesi - Yönetim ve Takip Sistemi ✨")
        self.root.geometry("1100x750") 
        
        # --- MODERN & UYUMLU RENK PALETİ ---
        self.RENK_ARKA_PLAN = "#F4F6F9"  
        self.RENK_ANA_ORION = "#1A365D"  
        self.RENK_KUTU_KITAP = "#E6FFFA" 
        self.RENK_KUTU_UYE = "#EBF8FF"   
        self.RENK_KUTU_ISLEM = "#FFFAF0" 
        
        # Buton Renkleri
        self.RENK_BTN_KITAP = "#234E52"  
        self.RENK_BTN_UYE = "#2B6CB0"    
        self.RENK_BTN_SIL = "#9B2C2C"    
        self.RENK_BTN_ODUNC = "#DD6B20"  
        self.RENK_BTN_IADE = "#319795"   
        self.RENK_YAZI_KOYU = "#2D3748"  

        self.root.configure(bg=self.RENK_ARKA_PLAN)
        self.kutuphane = Kutuphane()

        # Üst Başlık Paneli (Punto: 22)
        frame_baslik = tk.Frame(self.root, bg=self.RENK_ANA_ORION, pady=25)
        frame_baslik.pack(fill="x")
        
        lbl_baslik = tk.Label(
            frame_baslik, 
            text="✨ ORION KÜTÜPHANESİ DİJİTAL PANELİ ✨", 
            font=("Helvetica", 22, "bold"), 
            fg="#FFFFFF", 
            bg=self.RENK_ANA_ORION
        )
        lbl_baslik.pack()

        # Sekme Tasarımı (Punto: 15)
        self.stil = ttk.Style()
        self.stil.theme_use("default")
        self.stil.configure("TNotebook", background=self.RENK_ARKA_PLAN, borderwidth=0)
        self.stil.configure("TNotebook.Tab", font=("Helvetica", 15, "bold"), padding=[25, 12])
        self.stil.map("TNotebook.Tab",
                      background=[("selected", self.RENK_ANA_ORION), ("active", "#2A4365")],
                      foreground=[("selected", "#FFFFFF"), ("active", "#FFFFFF")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_kitap = tk.Frame(self.notebook, bg=self.RENK_ARKA_PLAN)
        self.tab_uye = tk.Frame(self.notebook, bg=self.RENK_ARKA_PLAN)
        self.tab_islem = tk.Frame(self.notebook, bg=self.RENK_ARKA_PLAN)

        self.notebook.add(self.tab_kitap, text="  📖 Kitap İşlemleri  ")
        self.notebook.add(self.tab_uye, text="  👥 Üye Yönetimi  ")
        self.notebook.add(self.tab_islem, text="  🔄 Ödünç / İade / Durum  ")

        self.tasarla_kitap_sekmesi()
        self.tasarla_uye_sekmesi()
        self.tasarla_islem_sekmesi()

    # --- 1. SEKME: KİTAP İŞLEMLERİ ---
    def tasarla_kitap_sekmesi(self):
        frame_ekle = tk.LabelFrame(
            self.tab_kitap, text="🎁 Kitap Kayıt ve Bağış Formu", 
            font=("Helvetica", 15, "bold"), fg=self.RENK_YAZI_KOYU, bg=self.RENK_KUTU_KITAP, padx=20, pady=25, bd=2
        )
        frame_ekle.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.EtiketEkle(frame_ekle, "Kitap ISBN 🔢:", 0, 0)
        self.ent_k_isbn = self.GirisKutusu(frame_ekle, 0, 1)

        self.EtiketEkle(frame_ekle, "Kitap Adı 📘:", 1, 0)
        self.ent_k_baslik = self.GirisKutusu(frame_ekle, 1, 1)

        self.EtiketEkle(frame_ekle, "Yazar Adı ✍️:", 2, 0)
        self.ent_k_yazar = self.GirisKutusu(frame_ekle, 2, 1)

        self.EtiketEkle(frame_ekle, "Kaç Adet 📊:", 3, 0)
        self.ent_k_adet = self.GirisKutusu(frame_ekle, 3, 1)
        self.ent_k_adet.insert(0, "1")

        btn_kitap_ekle = tk.Button(
            frame_ekle, text="➕ Kitabı Raflara Ekle", 
            font=("Helvetica", 14, "bold"), bg=self.RENK_BTN_KITAP, fg="#FFFFFF", 
            cursor="hand2", relief="raised", bd=2, pady=10, command=self.arayuz_kitap_ekle
        )
        btn_kitap_ekle.grid(row=4, column=0, columnspan=2, pady=25, sticky="ew")

        frame_liste = tk.LabelFrame(
            self.tab_kitap, text="📚 Mevcut Kitap Envanteri", 
            font=("Helvetica", 15, "bold"), fg=self.RENK_YAZI_KOYU, bg="#FFFFFF", padx=20, pady=20, bd=2
        )
        frame_liste.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.txt_kitaplar = tk.Text(frame_liste, width=50, height=14, font=("Courier New", 14, "bold"), bg="#FFFFFF", fg="#1A202C")
        self.txt_kitaplar.pack(side="left", fill="both", expand=True)
        
        scroll = tk.Scrollbar(frame_liste, command=self.txt_kitaplar.yview)
        scroll.pack(side="right", fill="y")
        self.txt_kitaplar.config(yscrollcommand=scroll.set)

        btn_yenile = tk.Button(
            self.tab_kitap, text="🔄 Rafları Güncelle", 
            font=("Helvetica", 12, "bold"), bg=self.RENK_ANA_ORION, fg="#FFFFFF", pady=5, command=self.arayuz_kitap_listele
        )
        btn_yenile.grid(row=1, column=1, pady=5, sticky="ew", padx=20)
        
        self.arayuz_kitap_listele()

    # --- 2. SEKME: ÜYE İŞLEMLERİ ---
    def tasarla_uye_sekmesi(self):
        frame_ekle = tk.LabelFrame(
            self.tab_uye, text="👥 Üye Ekleme / Silme İşlemleri", 
            font=("Helvetica", 15, "bold"), fg=self.RENK_YAZI_KOYU, bg=self.RENK_KUTU_UYE, padx=20, pady=25, bd=2
        )
        frame_ekle.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.EtiketEkle(frame_ekle, "Üye Kart ID 🪪:", 0, 0)
        self.ent_u_id = self.GirisKutusu(frame_ekle, 0, 1)

        self.EtiketEkle(frame_ekle, "Adı Soyadı 👤:", 1, 0)
        self.ent_u_isim = self.GirisKutusu(frame_ekle, 1, 1)

        self.EtiketEkle(frame_ekle, "E-Posta ✉️:", 2, 0)
        self.ent_u_eposta = self.GirisKutusu(frame_ekle, 2, 1)

        btn_uye_ekle = tk.Button(
            frame_ekle, text="🎉 Yeni Üye Kaydet", 
            font=("Helvetica", 13, "bold"), bg=self.RENK_BTN_UYE, fg="#FFFFFF", 
            cursor="hand2", relief="raised", bd=2, pady=8, command=self.arayuz_uye_ekle
        )
        btn_uye_ekle.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

        btn_uye_sil = tk.Button(
            frame_ekle, text="❌ Üyeliği Sistemden Sil", 
            font=("Helvetica", 13, "bold"), bg=self.RENK_BTN_SIL, fg="#FFFFFF", 
            cursor="hand2", relief="raised", bd=2, pady=8, command=self.arayuz_uye_sil
        )
        btn_uye_sil.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        frame_liste = tk.LabelFrame(
            self.tab_uye, text="👥 Kayıtlı Kitap Kurtları", 
            font=("Helvetica", 15, "bold"), fg=self.RENK_YAZI_KOYU, bg="#FFFFFF", padx=20, pady=20, bd=2
        )
        frame_liste.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.txt_uyeler = tk.Text(frame_liste, width=50, height=14, font=("Courier New", 14, "bold"), bg="#FFFFFF", fg="#1A202C")
        self.txt_uyeler.pack(side="left", fill="both", expand=True)
        
        scroll = tk.Scrollbar(frame_liste, command=self.txt_uyeler.yview)
        scroll.pack(side="right", fill="y")
        self.txt_uyeler.config(yscrollcommand=scroll.set)

        btn_yenile = tk.Button(
            self.tab_uye, text="🔄 Üye Listesini Yenile", 
            font=("Helvetica", 12, "bold"), bg=self.RENK_ANA_ORION, fg="#FFFFFF", pady=5, command=self.arayuz_uye_listele
        )
        btn_yenile.grid(row=1, column=1, pady=5, sticky="ew", padx=20)

        self.arayuz_uye_listele()

    # --- 3. SEKME: ÖDÜNÇ / İADE / SORGULAMA ---
    def tasarla_islem_sekmesi(self):
        frame_islem = tk.LabelFrame(
            self.tab_islem, text="🔄 Kitap Teslim ve İade Masası", 
            font=("Helvetica", 15, "bold"), fg=self.RENK_YAZI_KOYU, bg=self.RENK_KUTU_ISLEM, padx=25, pady=25, bd=2
        )
        frame_islem.pack(fill="x", padx=20, pady=15)

        self.EtiketEkle(frame_islem, "Üye Kart ID 🪪:", 0, 0)
        self.ent_islem_uye = self.GirisKutusu(frame_islem, 0, 1)

        self.EtiketEkle(frame_islem, "Kitap ISBN 🔢:", 1, 0)
        self.ent_islem_isbn = self.GirisKutusu(frame_islem, 1, 1)

        btn_odunc = tk.Button(
            frame_islem, text="📙 Ödünç Teslim Et", 
            font=("Helvetica", 13, "bold"), bg=self.RENK_BTN_ODUNC, fg="#FFFFFF", 
            width=22, pady=8, cursor="hand2", command=self.arayuz_odunc_ver
        )
        btn_odunc.grid(row=0, column=2, padx=25, pady=5)

        btn_iade = tk.Button(
            frame_islem, text="📗 Geri İade Al", 
            font=("Helvetica", 13, "bold"), bg=self.RENK_BTN_IADE, fg="#FFFFFF", 
            width=22, pady=8, cursor="hand2", command=self.arayuz_iade_al
        )
        btn_iade.grid(row=1, column=2, padx=25, pady=5)

        frame_sorgu = tk.LabelFrame(
            self.tab_islem, text="🔍 Akıllı Raf Müsaitlik Sorgulaması", 
            font=("Helvetica", 15, "bold"), fg=self.RENK_YAZI_KOYU, bg="#EDF2F7", padx=25, pady=25, bd=2
        )
        frame_sorgu.pack(fill="both", expand=True, padx=20, pady=15)

        self.EtiketEkle(frame_sorgu, "Aranacak ISBN 🔎:", 0, 0)
        self.ent_sorgu_isbn = self.GirisKutusu(frame_sorgu, 0, 1)

        btn_sorgu = tk.Button(
            frame_sorgu, text="Rafı Kontrol Et", 
            font=("Helvetica", 13, "bold"), bg=self.RENK_ANA_ORION, fg="#FFFFFF", padx=15, pady=5, command=self.arayuz_durum_sorgula
        )
        btn_sorgu.grid(row=0, column=2, padx=25, pady=5)

        self.frame_sonuc_kutu = tk.Frame(frame_sorgu, bg="#FFFFFF", bd=1, relief="solid", padx=20, pady=20)
        self.frame_sonuc_kutu.grid(row=1, column=0, columnspan=3, pady=20, sticky="ew")

        self.lbl_sorgu_sonuc = tk.Label(
            self.frame_sonuc_kutu, text="🔎 Sonuçları görmek için yukarıya geçerli bir ISBN yazıp sorgulayın.", 
            font=("Helvetica", 14, "italic"), bg="#FFFFFF", fg="#4A5568", justify="left", anchor="w"
        )
        self.lbl_sorgu_sonuc.pack(fill="x")

    def EtiketEkle(self, parent, metin, satir, sutun):
        lbl = tk.Label(parent, text=metin, font=("Helvetica", 15, "bold"), bg=parent.cget("bg"), fg=self.RENK_YAZI_KOYU)
        lbl.grid(row=satir, column=sutun, sticky="w", pady=10, padx=5)
        return lbl

    def GirisKutusu(self, parent, satir, sutun):
        ent = tk.Entry(parent, font=("Helvetica", 15), bd=2, relief="groove", width=24)
        ent.grid(row=satir, column=sutun, pady=10, padx=5, sticky="w")
        return ent

    # ================= İŞ MANTIĞI METOTLARI =================
    def arayuz_kitap_ekle(self):
        isbn = self.ent_k_isbn.get().strip()
        baslik = self.ent_k_baslik.get().strip()
        yazar = self.ent_k_yazar.get().strip()
        
        try:
            adet = int(self.ent_k_adet.get().strip() or 1)
            if adet <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata ❌", "Kitap adedi pozitif bir tam sayı olmalıdır!")
            return

        if isbn and baslik and yazar:
            self.kutuphane.kitap_bagis_al(isbn, baslik, yazar, adet)
            messagebox.showinfo("Başarılı 🎉", f"'{baslik}' Orion Kütüphanesi envanterine katıldı.")
            self.arayuz_kitap_listele()
            self.ent_k_isbn.delete(0, tk.END)
            self.ent_k_baslik.delete(0, tk.END)
            self.ent_k_yazar.delete(0, tk.END)
        else:
            messagebox.showwarning("Eksik Giriş ⚠️", "Lütfen tüm alanları doldurun.")

    def arayuz_kitap_listele(self):
        self.txt_kitaplar.config(state="normal")
        self.txt_kitaplar.delete("1.0", tk.END)
        if not self.kutuphane.kitaplar:
            self.txt_kitaplar.insert(tk.END, " Raflarda kitap bulunmuyor.")
        else:
            for k in self.kutuphane.kitaplar.values():
                info = f"📌 ISBN: {k.isbn}\n📘 Başlık: {k.baslik}\n✍️ Yazar: {k.yazar}\n📊 Stok: {k.adet} | 🟢 Müsait: {k.musait_adet}\n"
                info += "═"*30 + "\n"
                self.txt_kitaplar.insert(tk.END, info)
        self.txt_kitaplar.config(state="disabled")

    def arayuz_uye_ekle(self):
        uye_id = self.ent_u_id.get().strip()
        isim = self.ent_u_isim.get().strip()
        eposta = self.ent_u_eposta.get().strip()

        if uye_id and isim and eposta:
            if uye_id in self.kutuphane.uyeler:
                messagebox.showerror("Hata ❌", "Bu Üye ID zaten kayıtlı!")
                return
            self.kutuphane.uye_ekle(uye_id, isim, eposta)
            messagebox.showinfo("Başarılı 👍", f"'{isim}' sisteme başarıyla kaydedildi.")
            self.arayuz_uye_listele()
            self.ent_u_id.delete(0, tk.END)
            self.ent_u_isim.delete(0, tk.END)
            self.ent_u_eposta.delete(0, tk.END)
        else:
            messagebox.showwarning("Eksik Giriş ⚠️", "Lütfen tüm alanları doldurun.")

    def arayuz_uye_sil(self):
        uye_id = self.ent_u_id.get().strip()
        
        if not uye_id:
            messagebox.showwarning("Eksik ID ⚠️", "Lütfen silmek istediğiniz üyenin Üye Kart ID'sini yazın.")
            return
        
        if uye_id not in self.kutuphane.uyeler:
            messagebox.showerror("Hata ❌", "Sistemde bu ID numarasına ait bir üye bulunamadı!")
            return
        
        uye = self.kutuphane.uyeler[uye_id]
        if uye.odunc_alinanlar:
            messagebox.showerror("Silinemez ❌", f"'{uye.isim}' isimli üyenin üzerinde henüz iade etmediği kitaplar var! Önce kitapları iade almalısınız.")
            return
            
        onay = messagebox.askyesno("Emin misiniz? ❓", f"'{uye.isim}' kaydını tamamen silmek istediğinize emin misiniz?")
        if onay:
            del self.kutuphane.uyeler[uye_id]
            self.kutuphane.verileri_kaydet() 
            messagebox.showinfo("Silindi 🗑️", "Üye kaydı başarıyla silindi.")
            self.arayuz_uye_listele()
            self.ent_u_id.delete(0, tk.END)

    def arayuz_uye_listele(self):
        self.txt_uyeler.config(state="normal")
        self.txt_uyeler.delete("1.0", tk.END)
        if not self.kutuphane.uyeler:
            self.txt_uyeler.insert(tk.END, " Kayıtlı üye bulunmamaktadır.")
        else:
            for u in self.kutuphane.uyeler.values():
                kitaplar_str = ', '.join(u.odunc_alinanlar) if u.odunc_alinanlar else "Yok 🏖️"
                info = f"👤 Üye ID: {u.uye_id}\n📛 İsim: {u.isim}\n✉️ E-posta: {u.eposta}\n📖 Ödünçleri (ISBN): {kitaplar_str}\n"
                info += "═"*30 + "\n"
                self.txt_uyeler.insert(tk.END, info)
        self.txt_uyeler.config(state="disabled")

    def arayuz_odunc_ver(self):
        uye_id = self.ent_islem_uye.get().strip()
        isbn = self.ent_islem_isbn.get().strip()

        if not uye_id or not isbn:
            messagebox.showwarning("Eksik Giriş ⚠️", "Lütfen Üye ID ve ISBN alanlarını girin.")
            return

        if uye_id not in self.kutuphane.uyeler:
            messagebox.showerror("Hata ❌", "Üye bulunamadı!")
            return
        if isbn not in self.kutuphane.kitaplar:
            messagebox.showerror("Hata ❌", "Kitap bulunamadı!")
            return

        basarili = self.kutuphane.kitap_odunc_ver(uye_id, isbn)
        if basarili:
            messagebox.showinfo("Başarılı 🚀", "Kitap ödünç verildi.")
            self.arayuz_kitap_listele()
            self.arayuz_uye_listele()
        else:
            messagebox.showwarning("Hata ⚠️", "Kitap müsait değil ya da üye zaten bu kitabı almış.")

    def arayuz_iade_al(self):
        uye_id = self.ent_islem_uye.get().strip()
        isbn = self.ent_islem_isbn.get().strip()

        if not uye_id or not isbn:
            messagebox.showwarning("Eksik Giriş ⚠️", "Lütfen Üye ID ve ISBN alanlarını doldurun.")
            return

        if uye_id not in self.kutuphane.uyeler:
            messagebox.showerror("Hata ❌", "Üye bulunamadı!")
            return

        basarili = self.kutuphane.kitap_iade_al(uye_id, isbn)
        if basarili:
            messagebox.showinfo("Başarılı ✅", "Kitap iade alındı ve rafa eklendi.")
            self.arayuz_kitap_listele()
            self.arayuz_uye_listele()
        else:
            messagebox.showerror("Hata ❌", "Bu üye bu kitabı ödünç almamış!")

    def arayuz_durum_sorgula(self):
        isbn = self.ent_sorgu_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Eksik Giriş ⚠️", "Lütfen bir ISBN numarası yazın.")
            return

        if isbn in self.kutuphane.kitaplar:
            k = self.kutuphane.kitaplar[isbn]
            durum_metni = f"📖 Kitap Adı: {k.baslik}\n✍️ Yazar: {k.yazar}\n\n📊 Toplam Stok: {k.adet} Adet\n🔄 Şu An Ödünçte: {k.odunc_verilen} Adet\n✅ Rafta Müsait Olan: {k.musait_adet} Adet"
            
            if k.musait_adet > 0:
                self.lbl_sorgu_sonuc.config(text=f"🟢 MÜSAİT DURUMDA!\n\n{durum_metni}", fg="#22543D", font=("Helvetica", 14, "bold"))
            else:
                self.lbl_sorgu_sonuc.config(text=f"🔴 TÜM KOPYALAR ÖDÜNÇTE!\n\n{durum_metni}", fg="#742A2A", font=("Helvetica", 14, "bold"))
        else:
            self.lbl_sorgu_sonuc.config(text="❌ Aradığınız ISBN numarasına ait kitap Orion Kütüphanesi'nde bulunamadı.", fg="#742A2A", font=("Helvetica", 14, "bold"))


if __name__ == "__main__":
    root = tk.Tk()
    app = KutuphaneArayuz(root)
    root.mainloop()