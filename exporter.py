import os
from time import sleep

from KitronikAirQualityControlHAT import KitronikBME688, KitronikOLED
from prometheus_client import Gauge, start_http_server


class KitronikExporter:
    def __init__(self):
        self.temperature_gauge = Gauge("kitronik_temperature_celsius", "Temperature in Celsius")
        self.pressure_gauge = Gauge("kitronik_pressure_pa", "Pressure in Pascals")
        self.humidity_gauge = Gauge("kitronik_humidity_percent", "Relative Humidity in Percent")
        self.ec02_gauge = Gauge("kitronik_ec02_ppm", "eCO2 in PPM")
        self.air_quality_percent_gauge = Gauge(
            "kitronik_air_quality_percent", "Air Quality in Percent"
        )
        self.air_quality_score_gauge = Gauge("kitronik_air_quality_score", "Air Quality IAQ score")

        self.bme688 = KitronikBME688()
        self.oled = KitronikOLED()
        self.bme688.calcBaselines(self.oled)

    def update_metrics(self):
        self.bme688.measureData()
        temperature = self.bme688.readTemperature()
        pressure = self.bme688.readPressure()
        humidity = self.bme688.readHumidity()
        eco2 = self.bme688.readeCO2()
        aq_percent = self.bme688.getAirQualityPercent()
        aq_score = self.bme688.getAirQualityScore()

        self.temperature_gauge.set(temperature)
        self.pressure_gauge.set(pressure)
        self.humidity_gauge.set(humidity)
        self.ec02_gauge.set(eco2)
        self.air_quality_percent_gauge.set(aq_percent)
        self.air_quality_score_gauge.set(aq_score)

        self.oled.clear()
        self.oled.displayText(f"Temperature: {temperature}", 1)
        self.oled.displayText(f"Pressure: {pressure}", 2)
        self.oled.displayText(f"Humidity: {humidity}", 3)
        self.oled.displayText(f"eCO2: {eco2}", 4)
        self.oled.displayText(f"Air Quality %: {aq_percent}", 5)
        self.oled.displayText(f"Air Quality Score: {aq_score}", 6)
        self.oled.show()


if __name__ == "__main__":
    data_dir = os.environ.get("KITRONIK_DATA", ".")
    os.makedirs(data_dir, exist_ok=True)
    os.chdir(data_dir)

    start_http_server(8000)
    print("Exporter running on port 8000", flush=True)
    exporter = KitronikExporter()
    while True:
        exporter.update_metrics()
        sleep(30)
