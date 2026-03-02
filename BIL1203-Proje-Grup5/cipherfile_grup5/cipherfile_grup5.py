import tkinter as tk 
from tkinter import filedialog, messagebox
import os

from aes_sifreleme import AnaMotor
from xor_sifreleme import veri_koruyucu


secilenDosya_adresi = ""

window = tk.Tk()
secilenAlgoritma = tk.StringVar(value="AES")
window.title("Güvenli Şifreleme Uygulaması")
window.geometry("1000x650")
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
        
            dogrulama_isareti = b"XOR_OK"
            islem_verisi = dogrulama_isareti + ham_data
                
            final_hali = veri_koruyucu(islem_verisi, girilenSifre)
            
            cikti_adresi = secilenDosya_adresi + ".xor"
            with open(cikti_adresi, "wb") as cikti_dosyasi:
                cikti_dosyasi.write(final_hali)
                
            messagebox.showinfo("Başarili!", "XOR ile şifrelendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"XOR şifreleme hatasi: {e}")

#Sifre cözülen kisim.
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
                
            cozulmus_veri = veri_koruyucu(ham_data, girilenSifre)
            
            if not cozulmus_veri.startswith(b"XOR_OK"):
                messagebox.showerror("Hata!", "Yanliş Parola! Dosya deşifre edilemedi.")
                return

            temiz_veri = cozulmus_veri[6:]
            
            cikti_adresi = secilenDosya_adresi.replace(".xor", "") + "_cozuldu.txt"
            with open(cikti_adresi, "wb") as cikti_dosyasi:
                cikti_dosyasi.write(temiz_veri)
                
            messagebox.showinfo("Tebrikler", "XOR şifresi başariyla çözüldü!")
        except Exception as e:
            messagebox.showerror("Hata", f"XOR çözme hatasi: {e}")
            
# --- ARAYÜZ TASARIMI ---
tk.Label(window, text="Şifreleme Uygulamasına Hoşgeldiniz", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#00ff00").pack(pady=40)

# Dosya İşlemleri Bölümü
cerceve1 = tk.LabelFrame(window, text=" 1. Adım: Dosya Seçimi ", font=("Helvetica", 11, "bold"), padx=10, pady=10, bg="#252526", fg="white")
cerceve1.pack(pady=10, fill="x", padx=20)

tk.Button(cerceve1, text="Dosya Seç", command=dosyaSec, font=("Arial", 10, "bold"), bg="#007acc", fg="white").pack(pady=5)
dosyaBilgi = tk.Label(cerceve1, text="Dosya seçilmedi", font=("Arial", 9, "italic"), bg="#252526", fg="#bdc3c7")
dosyaBilgi.pack()

# Şifreleme İşlemleri Bölümü
cerceve2 = tk.LabelFrame(window, text=" 2. Adım: Şifreleme Ayarları ", font=("Helvetica", 11, "bold"), padx=10, pady=10, bg="#252526", fg="white")
cerceve2.pack(pady=10, fill="x", padx=20)

f_secenek = tk.Frame(cerceve2, bg="#252526")
f_secenek.pack(pady=5)
tk.Radiobutton(f_secenek, text="AES (Anahtarlı)", variable=secilenAlgoritma, value="AES", bg="#252526", fg="white", selectcolor="#1e1e1e").pack(side=tk.LEFT, padx=15)
tk.Radiobutton(f_secenek, text="XOR (Parolalı)", variable=secilenAlgoritma, value="XOR", bg="#252526", fg="white", selectcolor="#1e1e1e").pack(side=tk.LEFT, padx=15)

tk.Label(cerceve2, text="XOR Parolası (AES için boş bırakın):", bg="#252526", fg="#bdc3c7").pack()
sifreGirme = tk.Entry(cerceve2, show="*", font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
sifreGirme.pack(pady=5)

tk.Button(cerceve2, text="Şifreyi Oluştur", command=bosSifreleme, font=("Arial", 11, "bold"), bg="#27ae60", fg="white", width=25).pack(pady=5)
tk.Button(cerceve2, text="Şifreyi Çöz", command=bosSifrecozme, font=("Arial", 11, "bold"), bg="#c0392b", fg="white", width=25).pack(pady=5)

window.mainloop()