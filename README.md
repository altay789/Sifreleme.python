# Sifreleme.python
Bu proje, Python kullanarak geliştirilmiş, dosyaları güvenli bir şekilde şifrelemek ve geri çözmek için tasarlanmış bir masaüstü uygulamasıdır. Kullanıcı dostu bir arayüz üzerinden hem yüksek güvenlikli AES hem de hızlı XOR algoritmalarını destekler.

"cryptography" kütüphanesi kullanılarak dosya bazlı güvenli şifreleme ve bayt üzerinde XOR işlemleriyle kullanıcı tarafından belirlenen parola ile şifreleme sağlanır.
Kullanıcı arayüzü tkinter kütüphanesi ile geliştirilmiş olup dosya seçme, parola girişi alma ve işlem takibi yapabilme özelliklerine sahiptir.
Geçersiz anahtar veya bozuk dosya durumlarında kullanıcıyı bilgilendiren bir yapı kurulmuştur.

Gerekli kütüphaneleri:
pip install cryptography
komutuyla kurarak ve,
python arayüz.py
komutuyla uygulamayı başlatarak işlemlerinizi yapabilirsiniz.

*Şifrelemek veya deşifre etmek istediğiniz dosyayı seçiniz.
*Şifreleme algoritmanızı (AES - XOR) seçiniz.
*Gerekliyse parola girişi sağlayı işlemi başlatınız.
