import sqlite3
import time
import board
import adafruit_bme680
from datetime import datetime
import os

# Veritabanı dosyasının yolunu belirle
db_path = '/var/lib/grafana/sensor_data.db'  # /var/lib/grafana dizininde kaydediyoruz

# Veritabanı dizini yoksa oluştur (Bu işlemi root olarak yapmanız gerekebilir)
try:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
except PermissionError as e:
    print(f"Dizin oluşturulurken hata oluştu: {e}")
    print("Bu işlemi root olarak çalıştırmanız gerekebilir.")
    exit()

# BME680 sensörünü başlat
try:
    i2c = board.I2C()  # I2C haberleşme başlat
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    bme680.sea_level_pressure = 1013.25  # Deniz seviyesi basıncı
    print("BME680 sensörü başarıyla başlatıldı.")
except Exception as e:
    print(f"Sensör başlatılırken hata oluştu: {e}")
    exit()

# SQLite veritabanına bağlan veya oluştur
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Mevcut tabloyu sil
    cursor.execute('DROP TABLE IF EXISTS environment')
    conn.commit()
    print("Mevcut tablo silindi (varsa).")

    # Yeni tabloyu oluştur
    cursor.execute('''
    CREATE TABLE environment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        gas_resistance REAL,
        aqi REAL
    )
    ''')
    conn.commit()
    print(f"Veritabanına bağlanıldı ve yeni tablo oluşturuldu: {db_path}")
except sqlite3.Error as e:
    print(f"Veritabanı bağlantısı sırasında hata oluştu: {e}")
    exit()

# AQI hesaplama fonksiyonu
def calculate_aqi(humidity, gas_resistance):
    try:
        hum_weighting = 0.25  # Nem etkisi %25
        gas_weighting = 0.75  # Gaz etkisi %75
        hum_reference = 40  # Optimum nem referansı
        gas_lower_limit = 5000    # Kötü hava kalitesi sınırı
        gas_upper_limit = 50000   # İyi hava kalitesi sınırı

        # Nem skorunu hesapla
        if 38 <= humidity <= 42:
            hum_score = hum_weighting * 100  # Optimum nem skoru
        elif humidity < 38:
            hum_score = (hum_weighting / hum_reference) * humidity * 100
        else:
            hum_score = ((-hum_weighting / (100 - hum_reference) * humidity) + 0.416666) * 100

        # Gaz skorunu hesapla
        gas_resistance = max(min(gas_resistance, gas_upper_limit), gas_lower_limit)  # Sınırları uygula
        gas_score = (gas_weighting / (gas_upper_limit - gas_lower_limit) * gas_resistance -
                     (gas_lower_limit * (gas_weighting / (gas_upper_limit - gas_lower_limit)))) * 100

        # Nihai AQI skorunu hesapla
        air_quality_score = hum_score + gas_score

        return air_quality_score
    except Exception as e:
        print(f"AQI hesaplanırken hata oluştu: {e}")
        return 0

# Sonsuz döngü içinde verileri oku ve kaydet
while True:
    try:
        # Sensörden verileri oku
        temperature = bme680.temperature
        humidity = bme680.humidity
        pressure = bme680.pressure
        gas_resistance = bme680.gas
        aqi = calculate_aqi(humidity, gas_resistance)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Zaman damgası

        # Verileri konsola yazdır
        print(f"Zaman: {timestamp}, Sıcaklık: {temperature:.2f}°C, Nem: {humidity:.2f}%, Basınç: {pressure:.2f} hPa, Gaz Direnci: {gas_resistance:.2f} Ohm, AQI: {aqi:.2f}")

        # Veritabanına veriyi ekle
        cursor.execute('''
        INSERT INTO environment (time, temperature, humidity, pressure, gas_resistance, aqi)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, temperature, humidity, pressure, gas_resistance, aqi))
        conn.commit()
        print("Veri başarıyla veritabanına kaydedildi.")

        # Belirtilen süre kadar bekle
        time.sleep(300)  # 5 dakika
    except Exception as e:
        print(f"Döngü sırasında hata oluştu: {e}")
        time.sleep(5)  # Hata durumunda kısa bir süre bekle
