import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
import re


BASE_OUTPUT_FOLDER = "Cikti_Barkodlar"

class BarkodUretici:
    def __init__(self, root):
        self.root = root
        self.root.title("Otomatik Barkod Basıcı (İsimli & Klasörlü)")
        self.root.geometry("450x350")
        self.root.configure(bg="#f4f6f7")

   
        lbl_baslik = tk.Label(root, text="Barkod Oluşturucu V2", 
                              font=("Arial", 16, "bold"), bg="#f4f6f7", fg="#2c3e50")
        lbl_baslik.pack(pady=20)

       
        btn_ogrenci = tk.Button(root, text="👨‍🎓 Öğrenci Barkodlarını Bas", 
                                font=("Arial", 11, "bold"), bg="#3498db", fg="white", 
                                height=2, width=30, cursor="hand2",
                                command=self.bas_ogrenci)
        btn_ogrenci.pack(pady=15)

        btn_kitap = tk.Button(root, text="📚 Kitap Barkodlarını Bas", 
                              font=("Arial", 11, "bold"), bg="#e67e22", fg="white", 
                              height=2, width=30, cursor="hand2",
                              command=self.bas_kitap)
        btn_kitap.pack(pady=5)

      
        self.lbl_durum = tk.Label(root, text="Hazır - Dosya seçimi bekleniyor...", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#ecf0f1")
        self.lbl_durum.pack(side=tk.BOTTOM, fill=tk.X)

    def dosya_adi_temizle(self, isim):
        """
        Dosya adında olmaması gereken karakterleri temizler (?, /, *, :, vb.)
        """
        temiz_isim = re.sub(r'[\\/*?:"<>|]', "", str(isim))
        return temiz_isim.strip()

    def barkod_olustur(self, barkod_verisi, dosya_ismi, klasor_yolu):
        try:
            
            if not os.path.exists(klasor_yolu):
                os.makedirs(klasor_yolu)

            
            code128 = barcode.get_barcode_class('code128')
            writer = ImageWriter()
            
           
            my_barcode = code128(str(barkod_verisi), writer=writer)
            
           
            tam_yol = os.path.join(klasor_yolu, dosya_ismi)
            my_barcode.save(tam_yol)
            return True
        except Exception as e:
            print(f"Hata ({dosya_ismi}): {e}")
            return False

    def dosya_sec(self):
        return filedialog.askopenfilename(title="Excel Dosyasını Seç", filetypes=[("Excel Dosyaları", "*.xlsx")])

    def islem_yap(self, tip):
        dosya_yolu = self.dosya_sec()
        if not dosya_yolu:
            return

        self.lbl_durum.config(text="Dosya okunuyor...")
        self.root.update()

        try:
            df = pd.read_excel(dosya_yolu)
            
         
            col_kod = "Barkod"
            col_isim = "Ad"
            
         
            if tip == "OGRENCI":
                hedef_klasor = os.path.join(BASE_OUTPUT_FOLDER, "Ogrenci_Barkodlari")
            else:
                hedef_klasor = os.path.join(BASE_OUTPUT_FOLDER, "Kitap_Barkodlari")

          
            if col_kod not in df.columns or col_isim not in df.columns:
                messagebox.showerror("Hata", f"Excel dosyasında '{col_kod}' veya '{col_isim}' sütunları bulunamadı!")
                self.lbl_durum.config(text="Hata: Sütun isimleri uyuşmuyor.")
                return

            basarili = 0
            
            for index, row in df.iterrows():
                kod = row[col_kod]
                isim = row[col_isim]

               
                if pd.isna(kod) or str(kod).strip() == "":
                    continue
                
               
                if pd.isna(isim) or str(isim).strip() == "":
                    isim = f"Isimsiz_{kod}"

                
                temiz_isim = self.dosya_adi_temizle(isim)
                
                
                dosya_adi = temiz_isim 

                if self.barkod_olustur(kod, dosya_adi, hedef_klasor):
                    basarili += 1
                
                
                if index % 5 == 0:
                    self.lbl_durum.config(text=f"Basılıyor: {temiz_isim}")
                    self.root.update()

            messagebox.showinfo("Tamamlandı", f"{basarili} adet barkod oluşturuldu.\n\nKayıt Yeri:\n{os.path.abspath(hedef_klasor)}")
            self.lbl_durum.config(text="İşlem tamamlandı.")
            
           
            os.startfile(os.path.abspath(hedef_klasor))

        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmedik bir hata:\n{str(e)}")
            self.lbl_durum.config(text="Hata oluştu.")

    def bas_ogrenci(self):
        self.islem_yap("OGRENCI")

    def bas_kitap(self):
        self.islem_yap("KITAP")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarkodUretici(root)
    root.mainloop()