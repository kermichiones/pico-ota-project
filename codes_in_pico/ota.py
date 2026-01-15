# ota.py
import urequests
import os
import json
import machine
import time
import gc

# --- AYARLAR ---
# GitHub repository URL'nizi buraya yazin
BASE_URL = "https://raw.githubusercontent.com/kermichiones/pico-ota-project/main"
# ---------------

led = machine.Pin("LED", machine.Pin.OUT)

def clean_unused_files(manifest_files):
    # (Temizlik fonksiyonu ayni kaliyor)
    try:
        local_files = os.listdir("app")
        valid_filenames = []
        for item in manifest_files:
            if item["local"].startswith("app/"):
                valid_filenames.append(item["local"].split("/")[-1])
        for f in local_files:
            if f not in valid_filenames:
                try: os.remove("app/" + f)
                except: pass
    except: pass

def check_for_updates():
    print("OTA: Kontrol ediliyor...")
    
    # Eger Wi-Fi hic bagli degilse direkt cik
    # urequests hata verip programi patlatmasin
    import network
    if not network.WLAN(network.STA_IF).isconnected():
        print("OTA: Internet yok -> Guncelleme atlanıyor.")
        return

    try:
        # 1. Versiyon Kontrol (HATA YAKALAMA BLOGU ICINDE)
        try:
            remote_ver = urequests.get(BASE_URL + "/version.txt").text.strip()
            if "404" in remote_ver: raise ValueError("404")
        except Exception as e:
            print(f"OTA: Sunucuya ulasilamadi ({e}) -> Guncelleme atlanıyor.")
            return # Hata varsa cik, main.py devam etsin

        try:
            with open("version.txt", "r") as f:
                local_ver = f.read().strip()
        except:
            local_ver = "0.0.0"

        if remote_ver == local_ver:
            print("OTA: Cihaz zaten guncel.")
            return

        # 2. Guncelleme Var -> Indir
        print(f"OTA: Yeni surum bulundu ({remote_ver}). Indiriliyor...")
        led.on() # Indirme sirasinda sabit yak (veya blink)
        
        try:
            r = urequests.get(BASE_URL + "/manifest.json")
            manifest = json.loads(r.text)
            r.close()
            
            files = manifest.get("files", [])
            for item in files:
                # Indirirken LED blink
                led.toggle() 
                
                remote = item["remote"]
                local = item["local"]
                
                # Klasor ac
                if "/" in local:
                    try: os.mkdir(local.rsplit("/", 1)[0])
                    except: pass
                
                # .new teknigi (Internet koparsa eski dosya bozulmasin)
                dl = urequests.get(BASE_URL + "/" + remote)
                if dl.status_code == 200:
                    with open(local + ".new", "w") as f:
                        f.write(dl.text)
                    dl.close()
                    # Indirme basarili, simdi degistir
                    try: os.remove(local)
                    except: pass
                    os.rename(local + ".new", local)
                    print(f"OTA: OK -> {local}")
                else:
                    print(f"OTA: HATA -> {remote}")
                    dl.close()
                    # Kritik dosya inemediyse donguden cik, risk alma
                    return 
                
                gc.collect()
            
            clean_unused_files(files)

            # Basarili olduysa versiyonu yaz ve RESETLE
            with open("version.txt", "w") as f:
                f.write(remote_ver)
            
            print("OTA: Guncelleme TAMAM. Resetleniyor...")
            time.sleep(1)
            machine.reset()

        except Exception as e:
            print("OTA: Indirme sirasinda hata:", e)
            print("OTA: Risk almamak icin guncelleme iptal edildi.")
            # Reset ATMA. Eski kod hala saglam, devam et.
            return

    except Exception as e:
        print("OTA: Beklenmedik hata:", e)
        # Ne olursa olsun devam et
