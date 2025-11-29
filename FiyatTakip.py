import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os 

# --- AYARLAR ---

# 1. Takip edilecek ürünün URL'si (SENİN LİNKİNİ KOYDUM)
URL = "https://www.trendyol.com/lenovo/ideapad-slim-3-intel-i7-13620h-ddr5-16gb-512gb-freedos-14-inc-wuxga-aydinlatmali-klavye-83k0002atr-p-922449919?boutiqueId=61&merchantId=118352"

# 2. Tarayıcı kimliği (User-Agent) - DOKUNMA, BU İYİ
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

# 3. Fiyat bu seviyenin altına düşünce haber ver (KENDİNE GÖRE AYARLA)
ISTENEN_FIYAT = 24800.0  # Örnek olarak 20000 TL yazdım, burayı değiştir

# 4. E-posta Ayarları (BUNLARI DOLDURMAYI UNUTMA)
EMAIL_ADRESI = "mehmetdakkak042@gmail.com"      # Gönderen (Uygulama şifresi olan)
EMAIL_SIFRESI = "Antalya.63"  # 16 haneli uygulama şifresi
KIME_EMAIL = "mehmetdakkak040@gmail.com"     # Alarmın geleceği senin adresin

# --- GÜNCELLENMİŞ FONKSİYON ---

def fiyat_kontrol_et():
    try:
        # URL'nin soru işaretinden sonrasını temizleyip gösterelim (daha okunaklı olur)
        print(f"🔄 Ürün sayfası kontrol ediliyor: {URL.split('?')[0]}...")
        
        # 1. Adım: Web sitesine bağlan
        sayfa = requests.get(URL, headers=HEADERS)
        sayfa.raise_for_status() 
        print("✅ Bağlantı başarılı.")

        # 2. Adım: HTML'i parçala
        soup = BeautifulSoup(sayfa.content, "html.parser")

        # 3. Adım: Ürün başlığını çek (Trendyol için güncellendi)
        try:
            # Trendyol genelde ürün başlığı için h1 ve "pr-new-br-text" class'ını kullanır
            # SENİN İÇİN TAHMİNİ BULGU: <h1 class="pr-new-br-text">Lenovo Ideapad Slim 3...</h1>
            urun_basligi = soup.find("h1", {"class": "pr-new-br-text"}).get_text(strip=True)
            print(f"🏷️  Ürün: {urun_basligi[:50]}...")
        except AttributeError:
            print("⚠️ Ürün başlığı bulunamadı. Trendyol'un HTML class'ı değişmiş olabilir ('pr-new-br-text').")
            urun_basligi = "Başlık Bulunamadı"

        # 4. Adım: Fiyatı çek (Trendyol için güncellendi)
        try:
            # Trendyol indirimli fiyat için genelde "prc-dsc" class'lı span kullanır
            # SENİN İÇİN TAHMİNİ BULGU: <span class="prc-dsc">21.999 TL</span>
            fiyat_span = soup.find("span", {"class": "prc-dsc"})
            
            # Eğer indirimli fiyat (prc-dsc) yoksa, normal fiyata (prc-slg) bak
            if fiyat_span is None:
                print("İndirimli fiyat (prc-dsc) bulunamadı, normal fiyata (prc-slg) bakılıyor...")
                fiyat_span = soup.find("span", {"class": "prc-slg"})

            # Fiyatı metin olarak al ("21.999 TL")
            fiyat_str = fiyat_span.get_text(strip=True)
            
            # Fiyatı sayıya çevir ("21.999 TL" -> 21999.0)
            fiyat = float(fiyat_str.replace(".", "").replace(",", ".").split(" ")[0])
            print(f"💰 Şu anki Fiyat: {fiyat:,.2f} TL")
            
            # 5. Adım: Fiyatı karşılaştır
            if fiyat <= ISTENEN_FIYAT:
                print(f"\n🎉🎉 FİYAT DÜŞTÜ KANKA! 🎉🎉")
                print(f"İstediğin fiyat: {ISTENEN_FIYAT:,.2f} TL")
                print(f"Şu anki fiyat: {fiyat:,.2f} TL")
                email_gonder(urun_basligi, fiyat, URL)
            else:
                print(f"📉 Henüz değil. Hedef fiyat: {ISTENEN_FIYAT:,.2f} TL")
                
        except AttributeError:
            print("⚠️ Fiyat bilgisi bulunamadı. Trendyol'un fiyat class'ı (prc-dsc veya prc-slg) değişmiş olabilir.")
            print("Sayfayı 'İncele' ile kontrol etmen lazım.")
        except Exception as e:
            print(f"Fiyatı sayıya çevirirken hata: {e}")
            # fiyat_str tanımlanmamış olabilir, try bloğu dışına alalım
            fiyat_str_hata = ""
            if 'fiyat_span' in locals() and fiyat_span is not None:
                fiyat_str_hata = fiyat_span.get_text(strip=True)
            print(f"Çekilen ham fiyat metni: '{fiyat_str_hata}'")

    except requests.exceptions.HTTPError as errh:
        print(f"Http Hatası (Engellenmiş olabilirsin 403, 503 vb.): {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Bağlantı Hatası: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Zaman Aşımı Hatası: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Bilinmeyen Hata: {err}")

# ... (email_gonder fonksiyonu ve ana döngü kodun geri kalanıyla aynı) ...

# E-posta gönderme fonksiyonu (Değişiklik yok)
def email_gonder(urun, fiyat, urun_url):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADRESI, EMAIL_SIFRESI)
        
        subject = f"Fiyat Alarmi! {urun[:20]}... Fiyati Dustu!"
        body = f"Kanka selam,\n\nTakip ettigin urunun fiyati istedigin seviyeye indi!\n\nUrun: {urun}\nSu anki Fiyat: {fiyat:,.2f} TL\n\nHemen bak: {urun_url}"
        
        mesaj = f"Subject: {subject}\n\n{body}".encode('utf-8')
        
        server.sendmail(EMAIL_ADRESI, KIME_EMAIL, mesaj)
        print("✅ Fiyat alarm e-postası başarıyla gönderildi!")
        server.quit()
    except Exception as e:
        print(f"❌ E-posta gönderirken hata oluştu: {e}")
        print("E-posta ayarlarini (adres, uygulama şifresi) kontrol et.")

# --- ANA DÖNGÜ ---
if __name__ == "__main__":
    while True:
        fiyat_kontrol_et()
        # SİTEYİ YORMAMAK İÇİN SIK KONTROL ETME!
        # 1 saat = 3600 saniye
        bekleme_suresi = 60
        print(f"\n--- {int(bekleme_suresi/60)} dakika sonra tekrar kontrol edilecek ---")
        time.sleep(bekleme_suresi)