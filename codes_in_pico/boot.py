# boot.py
import network, time, machine, gc

# --- AYARLAR ---
SSID = "WIFI_ADI"
PASSWORD = "WIFI_SIFRESI"
# ---------------

led = machine.Pin("LED", machine.Pin.OUT)
led.on() # Acilista isik yansin (Ben buradayim mesaji)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Wi-Fi baglaniyor...", end="")
    # Sadece 10 saniye sans veriyoruz.
    # Baglanmazsa sistemi bekletmenin alemi yok.
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            print("\nWi-Fi BAGLANDI! IP:", wlan.ifconfig()[0])
            return True
        max_wait -= 1
        led.toggle() # Baglanirken goz kirp
        time.sleep(1)
    
    # Baglanamazsa:
    print("\nWi-Fi YOK. Offline modda devam ediliyor.")
    led.on() # Sabit yak
    return False

# GUVENLIK GECIKMESI (USB baglantisini kurtarmak icin 3 sn)
# Yanlis kod yuklersen Thonny'den durdurabilmen icin bu sure sart.
print("Sistem baslatiliyor... (Mudahele icin 3 sn)")
time.sleep(3)

connect_wifi()
# Wi-Fi baglansa da baglanmasa da islem biter, sira main.py'de.
