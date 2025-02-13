import sqlite3
import pandas as pd

# SQLite veritabanına bağlan
db_yolu = "/var/lib/grafana/sensor_data.db"
conn = sqlite3.connect(db_yolu)

# Tablo adını belirle
tablo_adi = "environment"  # Güncellenmiş tablo adı

# Verileri çek ve pandas DataFrame'e aktar
query = f"SELECT * FROM {tablo_adi}"
df = pd.read_sql_query(query, conn)

# Excel dosyasına kaydetme yolu (Masaüstü)
excel_dosyasi = "/home/musa/Desktop/sensor_verileri.xlsx"
df.to_excel(excel_dosyasi, index=False, engine="openpyxl")

# Bağlantıyı kapat
conn.close()

print(f"Veriler {excel_dosyasi} dosyasına kaydedildi.")
