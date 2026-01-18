import network
import urequests
import time
import machine
from machine import Pin, SPI, PWM
import gc

# st7735 kütüphanesi
try:
    import app.st7735 as st7735
except ImportError:
    import st7735

# ==========================================
# DONANIM AYARLARI
# ==========================================
# SPI ve Ekran Kurulumu
spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))

tft = st7735.TFT(spi, dc=14, reset=12, cs=13)
tft.init()

# Arka Işık
bl = PWM(Pin(15))
bl.freq(1000)
bl.duty_u16(40000)

# Renkler
WHITE = st7735.TFT.color565(255, 255, 255)
BLACK = st7735.TFT.color565(0, 0, 0)
GREEN = st7735.TFT.color565(0, 255, 0)
RED   = st7735.TFT.color565(255, 50, 50)
BLUE  = st7735.TFT.color565(50, 50, 255)
YELLOW = st7735.TFT.color565(255, 255, 0)

# Metni ekran genişliğine göre bölen fonksiyon
def wrap_text(text, max_chars=14):
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def get_quote():
    url = "https://dummyjson.com/quotes/random"
    try:
        # Bağlantı var mı diye hızlıca bir kontrol
        wlan = network.WLAN(network.STA_IF)
        if not wlan.isconnected():
            return "Wifi Bekleniyor...", "Sistem"

        print("API isteği atılıyor...")
        response = urequests.get(url)
        data = response.json()
        response.close()
        
        quote = data['quote']
        author = data['author']
        return quote, author
    except Exception as e:
        print("API Hatası:", e)
        return None, None

def display_quote(quote, author):
    if not quote: return

    tft.fill(BLACK)
    
    # Çerçeve
    tft.fill_rect(0, 0, 128, 128, BLUE)
    tft.fill_rect(2, 2, 124, 124, BLACK)
    
    # Başlık
    tft.text(5, 5, "GUNUN SOZU", YELLOW)
    tft.text(5, 15, "-"*14, YELLOW)
    
    # Sözü yazdır
    lines = wrap_text(quote, max_chars=14)
    y_pos = 30
    
    for line in lines:
        tft.text(8, y_pos, line, WHITE)
        y_pos += 10 
        if y_pos > 100: break
        
    # Yazar
    if author != "Sistem":
        tft.text(8, 110, f"- {author}", GREEN)
    else:
        tft.text(8, 110, f"{author}", RED)

# --- ANA DÖNGÜ ---
print("Sistem baslatildi, Wifi hazir varsayiliyor...")

# İlk açılış mesajı
tft.fill(BLACK)
tft.text(10, 50, "Baslatiliyor...", WHITE)
time.sleep(1)

while True:
    # 1. Sözü Çek
    quote, author = get_quote()
    
    if quote:
        display_quote(quote, author)
        print("Ekrana yazıldı.")
    else:
        # Hata durumunda ekrana bilgi ver
        tft.fill(BLACK)
        tft.text(10, 50, "Veri Alinamadi", RED)
        tft.text(10, 65, "Tekrar Deneniyor", WHITE)
    
    # Belleği temizle
    gc.collect()
    
    # 30 saniye bekle
    time.sleep(30)
