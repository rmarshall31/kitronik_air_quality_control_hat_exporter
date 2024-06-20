import signal
import sys
from KitronikAirQualityControlHAT import KitronikBME688, KitronikOLED
from prometheus_client import start_http_server, Gauge
from time import sleep


class KitronikExporter:
    def __init__(self):
        self.temperature_gauge = Gauge('kitronik_temperature_celsius', 'Temperature in Celsius')
        self.pressure_gauge = Gauge('kitronik_pressure_pa', 'Pressure in Pascals')
        self.humidity_gauge = Gauge('kitronik_humidity_percent', 'Relative Humidity in Percent')
        self.ec02_gauge = Gauge('kitronik_ec02_ppm', 'eCO2 in PPM')
        self.air_quality_percent_gauge = Gauge('kitronik_air_quality_percent', 'Air Quality in Percent')
        self.air_quality_score_gauge = Gauge('kitronik_air_quality_score', 'Air Quality IAQ score')

        self.bme688 = KitronikBME688()
        self.oled = KitronikOLED()
        self.bme688.calcBaselines(self.oled)

    def update_metrics(self):
        try:
            self.bme688.measureData()

            self.oled.clear()
            self.oled.displayText(f'Temperature: {self.bme688.readTemperature()}', 1)
            self.oled.displayText(f'Pressure: {self.bme688.readPressure()}', 2)
            self.oled.displayText(f'Humidity: {self.bme688.readHumidity()}', 3)
            self.oled.displayText(f'eCO2: {self.bme688.readeCO2()}', 4)
            self.oled.displayText(f'Air Quality %: {self.bme688.getAirQualityPercent()}', 5)
            self.oled.displayText(f'Air Quality Score: {self.bme688.getAirQualityScore()}', 6)
            self.oled.show()

            self.temperature_gauge.set(self.bme688.readTemperature())
            self.pressure_gauge.set(self.bme688.readPressure())
            self.humidity_gauge.set(self.bme688.readHumidity())
            self.ec02_gauge.set(self.bme688.readeCO2())
            self.air_quality_percent_gauge.set(self.bme688.getAirQualityPercent())
            self.air_quality_score_gauge.set(self.bme688.getAirQualityScore())
        except Exception as e:
            print(f'Error updating metrics: {e}')


def signal_handler(sig, frame):
    print('Shutting down exporter...')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    exporter = KitronikExporter()
    start_http_server(8000)
    print('Exporter running on port 8000')

    while True:
        exporter.update_metrics()
        sleep(30)
