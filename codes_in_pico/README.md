# Pico W OTA Project - Kurulum Rehberi

Bu klasördeki dosyalar, Raspberry Pi Pico W cihazınızı kesintisiz ve hataya dayanıklı (failsafe) bir şekilde çalışacak ve uzaktan güncellenebilecek hale getirmek için hazırlanmıştır.

## Yüklenecek Dosyalar

Aşağıdaki dosyaların hepsini Pico W cihazınızın ana dizinine yüklemelisiniz:

1.  **`boot.py`**: Wi-Fi bağlantısını yönetir. Bağlantı yoksa bile sistemi kilitlemeden devam ettirir.
2.  **`ota.py`**: GitHub üzerinden güncellemeleri kontrol eder. İnternet yoksa veya hata oluşursa sistemi bozmadan atlar.
3.  **`main.py`**: Ana kontrol dosyasıdır. Önce güncelleme kontrolü yapar, sonra uygulamanızı (`app/run.py`) başlatır.
4.  **`version.txt`**: Mevcut sürüm numarasını tutar. İlk yüklemede `0.0.0` olarak bırakabilirsiniz.
5.  **`app/` klasörü**: Uygulamanızın kodlarını barındırır.
    *   **`app/run.py`**: Sizin asıl çalışan kodunuzdur.

## Kurulum Adımları

1.  **Wi-Fi Ayarları:**
    *   `boot.py` dosyasını açın.
    *   `SSID` ve `PASSWORD` değişkenlerini kendi Wi-Fi ağ bilgilerinize göre düzenleyin.

2.  **Dosyaları Yükleme:**
    *   Thonny IDE veya benzeri bir araç kullanarak bu klasördeki (`codes_in_pico`) tüm dosyaları Pico W cihazınıza yükleyin.
    *   `app` klasörünü oluşturmayı ve içindeki `run.py` dosyasını da yüklemeyi unutmayın.

3.  **Sistemi Başlatma:**
    *   Pico'yu güçten çekip tekrar takın veya Thonny üzerinden "Run" butonuna basmadan önce reset atın (fişi çekip takmak en temizidir).

## Çalışma Mantığı

*   **Açılış:** Cihaz açıldığında `boot.py` çalışır ve 10 saniye boyunca Wi-Fi arar. Bulamazsa "Offline Mod"a geçer.
*   **Güncelleme:** `main.py`, `ota.py` modülünü çağırır. İnternet varsa GitHub'daki `version.txt` ile cihazdaki sürümü karşılaştırır.
    *   Yeni sürüm varsa indirir ve cihazı resetler.
    *   İnternet yoksa veya hata olursa bu adımı atlar.
*   **Uygulama:** Son olarak `main.py`, `app/run.py` dosyasını çalıştırır.

Bu yapı sayesinde, internet kesilse bile cihazınızdaki uygulama çalışmaya devam eder.
