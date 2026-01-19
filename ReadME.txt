# Kutuphane Otomasyon Sistemi V2

Python ve Tkinter kullanılarak geliştirilmiş, veritabanı olarak Excel dosyalarını kullanan masaüstü kütüphane yönetim uygulamasıdır. Küçük ölçekli kütüphaneler, okullar veya kişisel arşivler için tasarlanmıştır.

Bu sürüm (V2), önceki versiyonun üzerine geliştirilmiş olup, harici bir yazılıma ihtiyaç duymadan uygulama içerisinden barkod üretimi yapabilmektedir.

## Özellikler

* **Excel Tabanlı Veritabanı:** SQL kurulumu gerektirmez. Tüm veriler (öğrenci, kitap, ödünç kayıtları) proje klasöründeki Excel dosyalarında tutulur.
* **Entegre Barkod Üretici:** Code128 formatında kitap ve öğrenci barkodlarını PNG formatında oluşturur.
* **Gecikme Takibi:** Teslim tarihi yaklaşan veya geçen kitaplar listede renk kodları ile belirtilir.
* **Sınıf Atlatma:** Yıl sonu işlemleri için toplu sınıf yükseltme ve mezun etme fonksiyonu bulunur.

## Gereksinimler

Projenin çalışması için Python 3.x ve aşağıdaki kütüphanelerin yüklü olması gerekmektedir:

* openpyxl (Excel işlemleri için)
* pandas (Veri okuma işlemleri için)
* python-barcode (Barkod üretimi için)
* Pillow (Görsel işleme için)

## Kurulum

Projeyi bilgisayarınıza indirdikten sonra gerekli kütüphaneleri yüklemek için terminalde aşağıdaki komutu çalıştırın:

```bash
pip install openpyxl pandas python-barcode pillow