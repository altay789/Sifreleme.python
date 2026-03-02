import tkinter as tk 
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet, InvalidToken


# 1. AES MOTORU (Parolasız, Otomatik Anahtarlı)

class AnaMotor:
    def __init__(self) -> None:
        self._key: bytes | None = None
        self._motor: Fernet | None = None

    def key_olusturucu(self, key_konumu: str) -> None:
        self._key = Fernet.generate_key()
        self._motor = Fernet(self._key)
        with open(key_konumu, "wb") as key_dosyasi:
            key_dosyasi.write(self._key)

    def key_yukle(self, key_konumu: str) -> None:
        with open(key_konumu, "rb") as key_dosyasi:
            self._key = key_dosyasi.read().strip()
        try:
            self._motor = Fernet(self._key)
        except Exception as hata:
            self._key = None
            self._motor = None
            raise ValueError(f"Hata: '{key_konumu}' dosyasi bozuk veya geçerli bir key değil.") from hata

    def dosya_sifrele(self, girisin_konumu: str, cikisin_konumu: str) -> None:
        self._gerekli_key("dosya_sifrele")
        with open(girisin_konumu, "rb") as f:
            orjinal_metin = f.read()
        sifrelenmis_metin = self._motor.encrypt(orjinal_metin)
        with open(cikisin_konumu, "wb") as f:
            f.write(sifrelenmis_metin)

    def dosya_sifrelemeyi_ac(self, girisin_konumu: str, cikisin_konumu: str) -> None:
        self._gerekli_key("dosya_sifrelemeyi_ac")
        with open(girisin_konumu, "rb") as f:
            sifrelenmis_metin = f.read()
        try:
            orjinal_metin = self._motor.decrypt(sifrelenmis_metin)
        except InvalidToken as hata:
            raise ValueError("Şifre çözme başarisiz, dosya bozulmuş veya yanliş key yüklenmiş olabilir.") from hata
        with open(cikisin_konumu, "wb") as f:
            f.write(orjinal_metin)

    def _gerekli_key(self, islem: str) -> None:
        if self._motor is None:
            raise ValueError(f"Hata: AnaMotor.{islem}() işlemi bir key olmadan cagrildi.")


# 2. XOR algoritmasi

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


# 3. ARAYÜZ (GUI) VE BAĞLANTILAR

secilenDosya_adresi = ""

window = tk.Tk()
secilenAlgoritma = tk.StringVar(value="AES")
window.title("Şifreleme Uygulamasi")
window.geometry("1000x600")
window.configure(bg="#1e1e1e")

def dosyaSec():
    global secilenDosya_adresi
    adres = filedialog.askopenfilename(
        title="İşlem yapilacak dosyayi seçin:",
        filetypes=(("Tüm Dosyalar", "*.*"), ("Metin Dosyalari", "*.txt"))
    )
    if adres:
        secilenDosya_adresi = adres
        dosyaBilgi.config(text=f"Seçilen Dosya: {adres}")
    else:
        secilenDosya_adresi = ""
        dosyaBilgi.config(text="Dosya seçilmedi")

def bosSifreleme():
    algoritma = secilenAlgoritma.get()
    girilenSifre = sifreGirme.get()
    global secilenDosya_adresi

    if secilenDosya_adresi == "": 
        messagebox.showwarning("Hata!", "Önce şifrelenecek dosyayi seçiniz.")  
        return

    if algoritma == "AES":
        try:
            motor = AnaMotor()
            key_adresi = secilenDosya_adresi + ".key"
            cikti_adresi = secilenDosya_adresi + ".enc"
            
            motor.key_olusturucu(key_adresi)
            motor.dosya_sifrele(secilenDosya_adresi, cikti_adresi)
            
            messagebox.showinfo("Başarili!", f"AES ile şifrelendi!\n\nŞifreli Dosya: {cikti_adresi}\nOluşturulan Anahtar: {key_adresi}\n\nLÜTFEN ANAHTAR DOSYASINI GÜVENLİ BİR YERE KAYDEDİN!")
        except Exception as e:
            messagebox.showerror("Hata", f"AES şifreleme hatasi:\n{e}")

    elif algoritma == "XOR":
        if girilenSifre == "":
            messagebox.showwarning("Uyari", "XOR işlemi için bir şifre (parola) belirlemelisiniz!")
            return
        try:
            with open(secilenDosya_adresi, "rb") as dosya_nesnesi:
                ham_data = dosya_nesnesi.read()
                
            final_hali = veri_koruyucu(ham_data, girilenSifre)
            
            cikti_adresi = secilenDosya_adresi + ".xor"
            with open(cikti_adresi, "wb") as cikti_dosyasi:
                cikti_dosyasi.write(final_hali)
                
            messagebox.showinfo("Başarili!", f"XOR ile şifrelendi!\nKaydedildi: {cikti_adresi}")
        except Exception as e:
            messagebox.showerror("Hata", f"XOR şifreleme hatasi:\n{e}")

#Sifre ccözülen kisim.
def bosSifrecozme():
    algoritma = secilenAlgoritma.get()
    girilenSifre = sifreGirme.get()
    global secilenDosya_adresi

    if secilenDosya_adresi == "": 
        messagebox.showwarning("Hata!", "Önce şifresi çözülecek dosyayi seçiniz.")  
        return

    if algoritma == "AES":
        try:
            motor = AnaMotor()
            
            # 1. KULLANICIYA ANAHTAR SORDUĞUMUZ YER 
            messagebox.showinfo("Anahtar Gerekli", "Şifreyi çözmek için lütfen o dosyaya ait .key (anahtar) dosyasini seçin.")
            
            key_adresi = filedialog.askopenfilename(
                title="Şifreyi Çözmek İçin Anahtari Seçin",
                filetypes=(("Anahtar Dosyalari", "*.key"), ("Tüm Dosyalar", "*.*"))
            )
            
            # pencereyi çarpıdan kapatılırsa iptal etme kısmı bu
            if not key_adresi:
                messagebox.showwarning("İptal", "Anahtar seçilmediği için şifre çözme iptal edildi.")
                return

            # 2. ÇIKTI ADRESİNİ BELİRLE VE ÇÖZ
            cikti_adresi = secilenDosya_adresi.replace(".enc", "") + "_cozuldu.txt"
            
            motor.key_yukle(key_adresi)
            motor.dosya_sifrelemeyi_ac(secilenDosya_adresi, cikti_adresi)
            
            messagebox.showinfo("Tebrikler!", f"AES şifresi başariyla çözüldü!\nKaydedildi: {cikti_adresi}")
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu:\n{e}")

    elif algoritma == "XOR":
        if girilenSifre == "":
            messagebox.showwarning("Uyarı!", "XOR şifresini çözmek için parolanizi girmelisiniz.")
            return
        try:
            with open(secilenDosya_adresi, "rb") as dosya_nesnesi:
                ham_data = dosya_nesnesi.read()
                
            final_hali = veri_koruyucu(ham_data, girilenSifre)
            
            cikti_adresi = secilenDosya_adresi.replace(".xor", "") + "_cozuldu.txt"
            with open(cikti_adresi, "wb") as cikti_dosyasi:
                cikti_dosyasi.write(final_hali)
                
            messagebox.showinfo("Tebrikler", f"XOR şifresi başariyla çözüldü!\nKaydedildi: {cikti_adresi}")
        except Exception as e:
            messagebox.showerror("Hata", f"XOR çözme hatasi:\n{e}")

###Projemizin arayüz devami...
baslik = tk.Label(window, text="Sifrleme Uygulamasina Hosgeldiniz", font=("Arial", 15, "bold"), bg="#1e1e1e", fg="#00ff00")
baslik.pack(pady=40)

cerceveSecme = tk.LabelFrame(window, text=" Adi 1: Dosya İşlemleri ", font=("Helvetica", 13, "bold"), padx=10, pady=10, bg="#252526", fg="white")
cerceveSecme.pack(pady=10, fill="x", padx=20)

tk.Label(cerceveSecme, text="Aşağiaki butona tilayarak bir dosya seçin.", font=("Arial", 11, "bold"), bg="#252526", fg="white").pack(pady=5)
tk.Button(cerceveSecme, text="Dosya Seç", command=dosyaSec, font=("Arial", 11, "bold"), bg="#007acc", fg="white", cursor="hand2").pack(pady=5)

dosyaBilgi = tk.Label(cerceveSecme, font=("Arial", 10, "italic"), bg="#252526", fg="#bdc3c7", text="Dosya seçilmedi")
dosyaBilgi.pack(pady=5) 

cerceveSifreleme = tk.LabelFrame(window, text=" Adım 2: Şifreleme İşlemleri ", font=("Helvetica", 13, "bold"), padx=10, pady=10, bg="#252526", fg="white")
cerceveSifreleme.pack(pady=10, fill="x", padx=20)

secim_cercevesi = tk.Frame(cerceveSifreleme, bg="#252526")
secim_cercevesi.pack(pady=10)

tk.Radiobutton(secim_cercevesi, text="AES Şifreleme (Anahtar Dosyali)", variable=secilenAlgoritma, value="AES", bg="#252526", fg="white", selectcolor="#1e1e1e", cursor="hand2").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(secim_cercevesi, text="XOR Şifreleme (Parolali)", variable=secilenAlgoritma, value="XOR", bg="#252526", fg="white", selectcolor="#1e1e1e", cursor="hand2").pack(side=tk.LEFT, padx=10)

tk.Label(cerceveSifreleme, text="XOR için Parola Giriniz (AES için boş birakabilirsiniz):", font=("Arial", 10), bg="#252526", fg="#bdc3c7").pack(pady=5)
sifreGirme = tk.Entry(cerceveSifreleme, show="*", font=("Arial", 11, "bold"), bg="#333333", fg="white", insertbackground="white")
sifreGirme.pack(pady=5)

tk.Button(cerceveSifreleme, text="Şifreyi Oluştur", command=bosSifreleme, font=("Arial", 11, "bold"), bg="#27ae60", fg="white", padx=20, pady=5, cursor="hand2").pack(pady=5)
tk.Button(cerceveSifreleme, text="Şifreyi Çöz", command=bosSifrecozme, font=("Arial", 11, "bold"), bg="#c0392b", fg="white", padx=28, pady=5, cursor="hand2").pack(pady=5)

window.mainloop()