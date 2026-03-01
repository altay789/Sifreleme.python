import os

def xor_mekanizmasi(kaynak_veri, anahtar_kelime):
    """
    Bu fonksiyon, veriyi bayt düzeyinde XOR işlemine sokar.
    Simetrik yapısı sayesinde hem şifreler hem de çözer.
    """
    anahtar_bayt = anahtar_kelime.encode('utf-8')
    n = len(anahtar_bayt)
    
    # Her baytı sırasıyla anahtarın ilgili baytı ile XOR'luyoruz.
    islenmis_liste = bytearray()
    for sira, bayt in enumerate(kaynak_veri):
        yeni_bayt = bayt ^ anahtar_bayt[sira % n]
        islenmis_liste.append(yeni_bayt)
    
    return islenmis_liste

def proje_calistir(giris_dosyasi, cikis_dosyasi, sifre):
    try:
        # 1. Dosyayı oku (İkili/Binary Modda)
        if not os.path.exists(giris_dosyasi):
            print(f"Hata: {giris_dosyasi} bulunamadı!")
            return

        with open(giris_dosyasi, "rb") as f:
            ham_veri = f.read()

        # 2. XOR İşlemini Uygula
        sonuc = xor_mekanizmasi(ham_veri, sifre)

        # 3. Sonucu Yeni Dosyaya Yaz
        with open(cikis_dosyasi, "wb") as f:
            f.write(sonuc)

        print(f"--- BAŞARILI ---")
        print(f"'{giris_dosyasi}' işlendi ve '{cikis_dosyasi}' oluşturuldu.")

    except Exception as hata:
        print(f"Beklenmeyen bir hata: {hata}")


if __name__ == "__main__":
    GIZLI_ANAHTAR = "Bakircay_2026_Cipher" 

    proje_calistir("mesaj.txt", "sifreli.bin", GIZLI_ANAHTAR)
