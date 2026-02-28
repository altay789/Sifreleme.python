

import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox#bunu asıl algoritmları entegre etmediğimiz için örnek messagebox ekledim o algoritmlar yerine.

secilenDosya_adresi=""#bu ortak kullanağımız cep gibi birşey.
# eğer bunu yapmazsak sifreleme olusturdugumuzda acaba dosya secildi mi seçilmedi mi bilemez.






window=tk.Tk()
secilenAlgoritma = tk.StringVar(value="AES")#algoritma secimi icin yapilmisitir.
window.title("Sifreleme uygulamasi")
window.geometry("1000x600")
window.configure(bg="#1e1e1e")#koyu füme rengi bir arka plan.



def dosyaSec():
    global secilenDosya_adresi


    adres=filedialog.askopenfilename(
        title="Sifrelenecek dosyayi sec:",
        filetypes=(("Metin Dosyalari", "*.txt"), ("Tüm Dosyalar", "*.*"))
    )
    if adres:
       secilenDosya_adresi=adres

       dosyaBilgi.config(text=f"Seçilen Dosya: {adres}")

    else :
       secilenDosya_adresi=""#bu satıır eğer bir dosya secilmediyse bos labela dosya secilmedi yazısı koyulsun diye...
    
       dosyaBilgi.config(text="Dosya secilmedi")


def bosSifreleme():#bu isimleri kendim simdilik verdim.
   algoritma=secilenAlgoritma.get()

   girilenSifre=sifreGirme.get()


   if secilenDosya_adresi=="": 
       
    messagebox.showwarning("Hata!", " Önce sifrelenecek dosyayi seciniz. ")  

   elif girilenSifre=="":
      messagebox.showwarning("Uyari","Sifrelemediniz")

   else :

      if algoritma=="AES":
         # buraya AES kodu gelebilir.
         messagebox.showwarning("Tebrikler!","Sifre AES olusturuldu. ")
      
      
      

      elif algoritma=="XOR":
         #   buraya XOR kodu gelecek.
         messagebox.showwarning("Tebrikler","Sifre XOR ile olusturuldu.")

      






def bosSifrecozme():#bu isimleri kendim simdilik verdim.

   girilenSifre=sifreGirme.get()#tek bir entry var girilen sifreyi kaydediyoruz.

   if girilenSifre:#Eğer sifre girildiyse cozulecek demek bu satır.
      messagebox.showwarning("Tebrikler","Sifre cozuldu.")

   else :
      messagebox.showwarning("Uyari!","Sifre girmediniz .")
   
   



baslik=tk.Label(window,text="Sifreleme uygulamasina hosgeldiniz.",font=("Arial",15,"bold"),bg="#1e1e1e", fg="#00ff00")
baslik.pack(pady=90)

#Adım 1 in Cercevesi aşağıdaki.
cerceveSecme= tk.LabelFrame(window, text=" Adim 1: Dosya İslemleri ", font=("Helvetica", 13, "bold"), padx=10, pady=10, bg="#252526", fg="white")
cerceveSecme.pack(pady=10, fill="x", padx=20)

a=tk.Label(cerceveSecme,text="Asagidaki butona tklayarak bir dosya secin.",font=("Arial",11,"bold"),bg="#252526", fg="white")
a.pack(pady=5)

b=tk.Button(cerceveSecme,text="Dosya sec: ",command=dosyaSec,font=("Arial",11,"bold"),bg="#007acc", fg="white", cursor="hand2")
b.pack(pady=5)

dosyaBilgi=tk.Label(cerceveSecme,font=("Arial",10,"italic"),bg="#252526", fg="#bdc3c7")#bu kısım dosya secildikten sonra bu bos labela dosyanın.txtli kısmı gözükecek.
dosyaBilgi.pack(pady=5) #buraya kadarki cerceve mantığı dosya secme kısmıydı.



####### buradan sonraki cerceve mantığı dosya şifreleme mantığı+ şifreyi çzöme mantığı
cerceveSifreleme = tk.LabelFrame(window, text=" Adim 2: Sifreleme İslemleri ", font=("Helvetica", 13, "bold"), padx=10, pady=10,bg="#252526", fg="white")
cerceveSifreleme.pack(pady=10, fill="x",padx=20)

c=tk.Label(cerceveSifreleme,text="Sifrenizi giriniz:",font=("Arial",11,"bold"),bg="#252526", fg="white")
c.pack(pady=5)

sifreGirme=tk.Entry(cerceveSifreleme,show="*",font=("Arial",11,"bold"),bg="#333333", fg="white", insertbackground="white")
sifreGirme.pack(pady=5)

# Seçim kutularını yan yana koymak için görünmez bir kutu (Frame) oluşturuyoruz
secim_cercevesi = tk.Frame(cerceveSifreleme,bg="#252526")
secim_cercevesi.pack(pady=10)

# 1. Seçenek: AES
radio_aes = tk.Radiobutton(secim_cercevesi, text="AES Şifreleme", variable=secilenAlgoritma, value="AES",bg="#252526", fg="white", selectcolor="#1e1e1e", cursor="hand2")
radio_aes.pack(side=tk.LEFT, padx=10) # side=tk.LEFT yan yana dizilmelerini sağlar

# 2. Seçenek: XOR
radio_xor = tk.Radiobutton(secim_cercevesi, text="XOR Şifreleme", variable=secilenAlgoritma, value="XOR",bg="#252526", fg="white", selectcolor="#1e1e1e", cursor="hand2")
radio_xor.pack(side=tk.LEFT, padx=10)




sifreOlustur=tk.Button(cerceveSifreleme,text="Sifreyi olustur.",command=bosSifreleme,font=("Arial",11,"bold",),bg="#27ae60", fg="white", padx=20, pady=5, cursor="hand2")
sifreOlustur.pack(pady=5)

sifreCoz=tk.Button(cerceveSifreleme,text="Sifreyi coz.",command=bosSifrecozme, font=("Arial", 11, "bold"),bg="#c0392b", fg="white", padx=28, pady=5, cursor="hand2")
sifreCoz.pack(pady=5)






window.mainloop()