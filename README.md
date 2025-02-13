Bu Python betiği, BME680 hava kalitesi sensöründen alınan sıcaklık, nem, basınç ve gaz direnci verilerini SQLite veritabanına kaydeder. Ayrıca, hava kalitesi indeksi (AQI) hesaplayarak veritabanına ekler.
Gerekli kütüphaneyi kurun => pip install adafruit-circuitpython-bme680
Raspberry Pi için komutu çalıştırarak I2C'yi etkinleştirin: sudo raspi-config
