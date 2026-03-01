from cryptography.fernet import Fernet, InvalidToken


class AnaMotor:

    def __init__(self) -> None:
        self._key: bytes | None = None
        self._motor: Fernet | None = None

    # Key İşlemleri

    def key_olusturucu(self, key_konumu: str) -> None:
        self._key = Fernet.generate_key()
        self._motor = Fernet(self._key)

        with open(key_konumu, "wb") as key_dosyasi:
            key_dosyasi.write(self._key)

        print(f"Key oluşturulup kaydedildi. '{key_konumu}'")

    def key_yukle(self, key_konumu: str) -> None:
        
        with open(key_konumu, "rb") as key_dosyasi:
            self._key = key_dosyasi.read().strip()

        try:
            self._motor = Fernet(self._key)
        except Exception as hata:
            self._key = None
            self._motor = None
            raise ValueError(
                f"Hata: '{key_konumu}' dosyasi bozuk veya geçerli bir key değil."
            ) from hata

        print(f"Key yüklendi. '{key_konumu}'")

    # Dosya İşlemleri

    def dosya_sifrele(self, girisin_konumu: str, cikisin_konumu: str) -> None:
        
        self._gerekli_key("dosya_sifrele")

        with open(girisin_konumu, "rb") as f:
            orjinal_metin = f.read()

        sifrelenmis_metin = self._motor.encrypt(orjinal_metin)

        with open(cikisin_konumu, "wb") as f:
            f.write(sifrelenmis_metin)

        print(
            f" Şifrelendi! '{girisin_konumu}' > '{cikisin_konumu}' "
            f"({len(orjinal_metin)} bytes > {len(sifrelenmis_metin)} bytes)"
        )

    def dosya_sifrelemeyi_ac(self, girisin_konumu: str, cikisin_konumu: str) -> None:
        
        self._gerekli_key("dosya_sifrelemeyi_ac")

        with open(girisin_konumu, "rb") as f:
            sifrelenmis_metin = f.read()

        try:
            orjinal_metin = self._motor.decrypt(sifrelenmis_metin)
        except InvalidToken as hata:
            raise ValueError(
                "Sifre cozme basarisiz, dosya bozulmus veya yanlis key girisi yapilmis olunabilinir."
            ) from hata

        with open(cikisin_konumu, "wb") as f:
            f.write(orjinal_metin)

        print(
            f" Sifre cozuldu '{girisin_konumu}' > '{cikisin_konumu}' "
            f"({len(sifrelenmis_metin)} bytes > {len(orjinal_metin)} bytes)"
        )

    # Yardımcı Fonksiyonlar

    def _gerekli_key(self, islem: str) -> None:
        
        if self._motor is None:
            raise ValueError(
                f"Hata: AnaMotor.{islem}() işlemi bir key olmadan cagrildi."
            )

# Test ve Demo Bloğu

if __name__ == "__main__":
    print("\n--- Uygulama Testi ---")

    # 1. Test dosyaları için isimlendirme
    orijinal_dosya = "test_orijinal.txt"
    sifreli_dosya = "test_sifreli.enc"
    cozulmus_dosya = "test_cozulmus.txt"
    anahtar_dosyasi = "test_anahtari.key"

    # Sahte bir metin dosyası yaratma
    with open(orijinal_dosya, "w", encoding="utf-8") as f:
        f.write("Bu gizli bir mesajdir.")
    
    print("\n1 - Test dosyasi oluşturuldu.")

    # 2. Motoru çalıştır ve key üret
    motor = AnaMotor()
    print("2 - Yeni key üretiliyor.")
    motor.key_olusturucu(anahtar_dosyasi)

    # 3. Dosyayı şifrele
    print("\n3 - Dosya şifreleniyor.")
    motor.dosya_sifrele(orijinal_dosya, sifreli_dosya)

    # 4. Dosyayı deşifre et
    print("4 - Dosya deşifre ediliyor.")
    motor.dosya_sifrelemeyi_ac(sifreli_dosya, cozulmus_dosya)

    print("--- Test Basarili ---\n")