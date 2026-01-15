# main.py
import machine
import time
import ota

led = machine.Pin("LED", machine.Pin.OUT)

def safe_panic(msg):
    print("KRITIK UYGULAMA HATASI:", msg)
    # PC baglantisini kesmemek icin yavas blink
    while True:
        led.toggle()
        time.sleep(1.0) 

# --- 1. OTA DENEMESI ---
# Burasi "try-except" icinde olmasa bile ota.py kendi icinde hatalari yutuyor.
# Yine de cift dikis atalim.
try:
    ota.check_for_updates()
except Exception as e:
    print("Main: OTA modulu genel hatasi:", e)

# --- 2. UYGULAMAYI BASLAT ---
print("Main: Uygulama baslatiliyor...")

# Eger her sey yolundaysa LED KAPALI olmali.
led.off()

try:
    import app.run
except ImportError:
    safe_panic("app/run.py dosyasi yok! (Ilk yukleme yapilmadi mi?)")
except Exception as e:
    safe_panic("Kod calisirken coktu: " + str(e))
