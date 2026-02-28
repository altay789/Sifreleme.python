import os


def veri_koruyucu(ana_bilgi, kilit_anahtari):
    """
    Bu fonksiyon, veriyi bayt düzeyinde XOR ile şifreler.
        """
    # Şifreyi (anahtar) sayısal baytlara çeviriyoruz
    anahtar_baytlari = kilit_anahtari.encode('utf-8')
    anahtar_uzunlugu = len(anahtar_baytlari)
    
    # Veriyi doğrudan üzerinde işlem yapabileceğimiz bir yapıya alıyoruz
    islenmis_cikti = bytearray(ana_bilgi)
    
    
    adim = 0  
     
    while True:
        # Eğer dosyanın son baytına geldiysek döngüyü kır
        if adim >= len(islenmis_cikti):
            break 
            
        # Mod işlemi ile anahtarı dosya boyuna yayıyoruz
        anahtar_konumu = adim % anahtar_uzunlugu
        secilen_maske = anahtar_baytlari[anahtar_konumu]
        
        # XOR İŞLEMİ: 
        islenmis_cikti[adim] = islenmis_cikti[adim] ^ secilen_maske
        
        # Bir sonraki adıma geç
        adim += 1 
        
    return islenmis_cikti

# --- DOSYA VE SİSTEM YÖNETİMİ ---
def islemi_baslat(giris_yolu, cikis_yolu, parola):
    try:
        # Dosyanın bilgisayarda olup olmadığını kontrol et
        if os.path.exists(giris_yolu):
            
            # Dosyayı ikili (binary) modda aç ve oku
            with open(giris_yolu, "rb") as dosya_nesnesi:
                ham_data = dosya_nesnesi.read()
            
            # Ana fonksiyonu çalıştır.
            final_hali = veri_koruyucu(ham_data, parola)
            
            # Sonucu yeni bir isimle kaydet
            with open(cikis_yolu, "wb") as cikti_dosyasi:
                cikti_dosyasi.write(final_hali)
            
            print(">> [SİSTEM]: Veri koruma işlemi başarıyla tamamlandı.")
            print(f">> [BİLGİ]: '{cikis_yolu}' dosyası oluşturuldu.")
        else:
            print("HATA: 'mesaj.txt' bulunamadı!")
            
    except Exception as hata:
        # Herhangi bir hatada uyarı mesajı verir.
        print(f"Sistemsel bir hata oluştu: {hata}")

# --- PROGRAMIN GİRİŞ NOKTASI ---
if __name__ == "__main__":
    # Şifremiz
    GIZLI_PAROLA = "Proje5_Grup5*" 
    
    # Uygulamayı çalıştır: Girdi -> Çıktı -> Şifre
    islemi_baslat("mesaj.txt", "sifreli.bin", GIZLI_PAROLA)