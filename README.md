Proje Açıklaması
Bu Python betiği, BME680 hava kalitesi sensöründen alınan sıcaklık, nem, basınç ve gaz direnci verilerini SQLite veritabanına kaydeder. Ayrıca, hava kalitesi indeksi (AQI) hesaplayarak veritabanına ekler. Bu veriler daha sonra Grafana ile görselleştirilebilir.

Gerekli Kütüphaneler
İlk olarak, Adafruit CircuitPython BME680 sensör kütüphanesini kurmamız gerekiyor. Bunun için aşağıdaki komutu çalıştırabilirsiniz:
pip install adafruit-circuitpython-bme680

Raspberry Pi İçin I2C Etkinleştirme
BME680 sensörü I2C arayüzünü kullanır, bu yüzden I2C'yi etkinleştirmeniz gerekmektedir. Aşağıdaki komutu çalıştırarak raspi-config aracını kullanarak I2C'yi etkinleştirebilirsiniz:
sudo raspi-config
Interfacing Options menüsüne gidin.
I2C seçeneğini seçin ve etkinleştirin.
Raspberry Pi'nizi yeniden başlatın.

Veritabanı Yapılandırması
Python betiği, sensörden alınan verileri SQLite veritabanına kaydedecektir. SQLite veritabanı dosyasının oluşturulacağı dizinde aşağıdaki komutları çalıştırabilirsiniz:

Grafana Kurulumu ve Yapılandırması
Grafana, veritabanınızdan verileri görselleştirmenize olanak tanır. Aşağıdaki adımlarla Grafana'yı Raspberry Pi'ye kurabilirsiniz:

Grafana'yı Yükleyin:
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get install grafana
Grafana'yı Başlatın ve Otomatik Olarak Başlatılacak Şekilde Ayarlayın:
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
Grafana Web Arayüzüne Erişin:
Grafana, http://localhost:3000 adresinden erişilebilir. İlk giriş için kullanıcı adı ve şifreyi admin olarak girmeniz gerekecek. Şifreyi değiştirmeyi unutmayın.

Veritabanı Bağlantısını Yapın:
Grafana web arayüzünde, Data Sources kısmına gidin ve SQLite veri kaynağını ekleyin. sensor_data.db dosyasını seçerek bağlanın.

Dashboard Oluşturun:
Grafana'da yeni bir dashboard oluşturun ve veritabanınızdan verileri çekmek için sorgular yazın. Sıcaklık, nem, basınç ve AQI gibi parametreler için görselleştirmeler ekleyebilirsiniz.
