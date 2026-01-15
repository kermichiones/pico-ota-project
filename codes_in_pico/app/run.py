# app/run.py
import time
from machine import Pin

# LED'i yakip sondurme.
# Anlasmamaz "Her sey yolundaysa LED kapali kalsin" idi.
# Ama kodun calistigini gormen icin log basiyoruz.

print("--- UYGULAMA BASLADI (v1.0.0) ---")

sayac = 0
while True:
    print(f"Sistem Calisiyor... Sayac: {sayac}")
    sayac += 1
    
    # Burada sensor okuma vs yapabilirsin.
    # Eger internet varsa veri gonderirsin, yoksa hafizaya yazarsin.
    
    time.sleep(5)
