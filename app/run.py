import machine
import time
from machine import Pin, SPI, PWM
try:
    import app.st7735 as st7735
except ImportError:
    import st7735

# SPI Ayarları
spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))

tft = st7735.TFT(spi, dc=14, reset=12, cs=13)
tft.init()

# Arka ışık
bl = PWM(Pin(15))
bl.freq(1000)
bl.duty_u16(40000)

# Renk Tanımları
RED = st7735.TFT.color565(255, 0, 0)
GREEN = st7735.TFT.color565(0, 255, 0)
BLUE = st7735.TFT.color565(0, 0, 255)
YELLOW = st7735.TFT.color565(255, 255, 0)
BLACK = st7735.TFT.color565(0, 0, 0)

# Test edilecek kombinasyonlar: (X_Offset, Y_Offset, Renk)
tests = [
    (0, 0, RED),    # 1. Kirmizi
    (2, 1, GREEN),  # 2. Yesil
    (2, 3, BLUE),   # 3. Mavi (Genelde budur)
    (1, 2, YELLOW)  # 4. Sari
]

while True:
    for x, y, color in tests:
        # Offseti ayarla
        tft._offset = (x, y)
        
        # Ekrani o renge boya
        tft.fill(color)
        
        # İçine siyah bir kutu çiz ki kenar kalınlığı belli olsun
        # Ekranda 1 piksel kalınlığında renkli çerçeve kalmalı
        tft.fill_rect(1, 1, 126, 126, BLACK)
        
        # Ortaya küçük bir kutu
        tft.fill_rect(60, 60, 8, 8, color)

        # 4 Saniye bekle (İncelemen için)
        time.sleep(4)
