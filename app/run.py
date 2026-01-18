import time
import math
import random
from machine import Pin, SPI, PWM
try:
    import app.st7735 as st7735
except ImportError:
    import st7735

# --- SETUP ---
print("Ekran Başlatılıyor (Initializing)...")

spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))

tft = st7735.TFT(spi, dc=14, reset=12, cs=13)
tft.init()

# Arka Işık (Backlight)
bl = PWM(Pin(15))
bl.freq(1000)
bl.duty_u16(40000) 

print("Ekran hazır.")

def color_wheel(pos):
    if pos < 85:
        return st7735.TFT.color565(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return st7735.TFT.color565(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return st7735.TFT.color565(0, pos * 3, 255 - pos * 3)

def cool_graphics_demo():
    # 1. TEST: KIRMIZI ÇERÇEVE (Hizalama kontrolü için en iyisi)
    # Eğer offset yanlışsa bu çerçevenin bir kenarı görünmez veya gürültülü olur.
    tft.fill(st7735.TFT.color565(255, 0, 0)) # Tam ekran kırmızı
    tft.fill_rect(1, 1, 126, 126, 0)         # İçini siyah yap (1px çerçeve kalır)
    time.sleep(1)

    center_x = 64
    center_y = 64
    
    # Genişleyen Daireler
    for i in range(8):
        color = color_wheel((i * 25) % 255)
        tft.fill_rect(center_x - i*6, center_y - i*6, i*12, i*12, color)
        time.sleep(0.05)

    tft.fill(0)
    
    # Rastgele Kutular
    for i in range(20):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        w = random.randint(10, 28)
        h = random.randint(10, 28)
        c = st7735.TFT.color565(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        tft.fill_rect(x, y, w, h, c)
        time.sleep(0.02)

    # Matrix Tarzı Noktalar
    tft.fill(0)
    for i in range(100):
        x = random.randint(0, 127)
        y = random.randint(0, 127)
        c = st7735.TFT.color565(100, 255, 100)
        tft.pixel(x, y, c)
        
    time.sleep(0.5)

# --- ANA TEST DÖNGÜSÜ ---
# En yaygın ST7735 kayma değerleri buradadır.
# Sırayla bunları dener.
offsets_to_test = [
    (0, 0),  # Varsayılan
    (2, 3),  # En yaygın kayma (Green Tab 128x128)
    (2, 1),  # Bazı Black Tab ekranlar
    (3, 2)   # Nadir durumlar
]

while True:
    for x_off, y_off in offsets_to_test:
        # 1. Konsola neyi test ettiğimizi yazalım
        print(f"----------------------------------------")
        print(f"ŞU AN TEST EDİLİYOR -> Offset X: {x_off}, Y: {y_off}")
        print(f"Lütfen ekrandaki kırmızı çerçeveye bak.")
        
        # 2. Offset'i anlık olarak değiştirelim
        tft._offset = (x_off, y_off)
        
        # 3. Grafikleri çalıştır
        cool_graphics_demo()
        
        time.sleep(1)
