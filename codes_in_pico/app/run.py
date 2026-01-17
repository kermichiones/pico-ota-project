import time
import math
import random
from machine import Pin, SPI, PWM
try:
    import app.st7735 as st7735
except ImportError:
    import st7735

# --- SETUP ---
# SPI0
# SCK -> 18
# SDA/MOSI -> 19
# RES -> 12
# DC -> 14
# CS -> 13
# LED -> 15

print("Initializing Display...")

spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))

tft = st7735.TFT(spi, dc=14, reset=12, cs=13)
tft.init()

# Backlight
bl = PWM(Pin(15))
bl.freq(1000)
bl.duty_u16(40000) # Brightness

print("Display initialized.")

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
    print("Starting graphics demo...")
    tft.fill(0) # Clear black

    center_x = 64
    center_y = 64
    radius = 50
    
    # Expanding circles
    for i in range(10):
        color = color_wheel((i * 25) % 255)
        tft.fill_rect(center_x - i*5, center_y - i*5, i*10, i*10, color)
        time.sleep(0.1)

    tft.fill(0)
    
    # Random rects
    for i in range(50):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        w = random.randint(10, 28)
        h = random.randint(10, 28)
        c = st7735.TFT.color565(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        tft.fill_rect(x, y, w, h, c)
        time.sleep(0.05)

    # Hyperspace lines
    tft.fill(0)
    for i in range(100):
        x = random.randint(0, 128)
        y = random.randint(0, 128)
        c = st7735.TFT.color565(100, 255, 100) # Green matrix style
        tft.pixel(x, y, c)
        # Fake "line" by drawing a few more
        tft.pixel(x+1, y+1, c)
        
    time.sleep(1)

# Main Loop
while True:
    cool_graphics_demo()
    time.sleep(2)
