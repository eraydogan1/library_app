Okul Kütüphanesi Yönetim Sistemi

Bu proe, okullarda kullanılan kütüphaneler için geliştirilmiş masaüstü tabanlı bir yönetim sistemidir. Python ve Tkinter kullanılarak geliştirilmiştir ve veriler Excel dosyaları üzerinden saklanmaktadır.

Özellikler

Öğrenci ekleme, listeleme ve silme

Kitap ekleme (çoklu kopya desteği ile), listeleme ve silme

Kitap ödünç verme ve teslim alma işlemleri

Ödünçte olan kitapların listelenmesi

Öğrenci bazlı kitap kullanım performans raporu

Teslim edilen kitapların detaylı raporlanması

Kitap adı, kitap ID, öğrenci adı veya öğrenci numarası ile arama

Kullanıcı dostu sekmeli arayüz

Kullanılan Teknolojiler

Python 3

Tkinter (GUI)

openpyxl (Excel dosya işlemleri)

Dosya Yapısı

ogrenciler.xlsx : Öğrenci bilgileri

kitaplar.xlsx : Kitap ve kopya bilgileri

odunc.xlsx : Ödünç işlemleri

teslim.xlsx : Teslim edilen kitap kayıtları

Bu dosyalar uygulama ilk çalıştırıldığında otomatik olarak oluşturulur.

Kurulum

Python 3 yüklü olduğundan emin olun

Gerekli kütüphaneyi yükleyin:

pip install openpyxl


Projeyi çalıştırın:

python main.py

Kullanım

“Öğrenci / Kitap Ekle” sekmesinden yeni kayıtlar oluşturabilirsiniz

“Ödünç / Teslim” sekmesinden kitap işlemlerini yapabilirsiniz

“Raporlar” sekmesinden aktif ödünçler ve öğrenci performanslarını görüntüleyebilirsiniz

“Arama / Silme” sekmesinden filtreleme ve kayıt silme işlemleri yapılabilir