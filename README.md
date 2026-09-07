# Kitronik Air Quality Control HAT Prometheus exporter

Reads the [Kitronik Air Quality Control HAT](https://kitronik.co.uk/products/5038-kitronik-air-quality-control-hat-for-raspberry-pi)
BME688 on a Raspberry Pi, exposes Prometheus gauges on TCP 8000, and mirrors
the same values on the HAT OLED.

Not a Kitronik product. The vendor library is MIT; this repo is MIT as well.

## Hardware

64-bit Raspberry Pi OS, HAT seated, serial hardware enabled (`raspi-config` →
Interface Options → Serial Port: login shell No, serial hardware Yes).

The container is privileged and bind-mounts `/dev/gpiomem` and `/dev/mem`
because the Kitronik Python stack uses `RPi.GPIO` and SMBus. That is a full
host compromise path if the container is reachable; keep it on the Pi's LAN.

## Metrics

| Name | Meaning |
| --- | --- |
| `kitronik_temperature_celsius` | BME688 temperature |
| `kitronik_pressure_pa` | Pressure (Pa) |
| `kitronik_humidity_percent` | Relative humidity |
| `kitronik_ec02_ppm` | Estimated CO2 (ppm) |
| `kitronik_air_quality_percent` | Vendor air-quality percent |
| `kitronik_air_quality_score` | Vendor IAQ score |

Scrape `http://<pi>:8000/metrics`. Values update every 30s. There is no
AirNow AQI mapping.

## Run

```bash
docker build --platform linux/arm64 -t kitronik_exporter .
docker run --privileged \
  -v /dev/gpiomem:/dev/gpiomem \
  -v /dev/mem:/dev/mem \
  -v kitronik-data:/var/lib/kitronik \
  -p 8000:8000 kitronik_exporter
```

Or pull the published arm64 image (public after the first GHCR package is
set to public):

```bash
docker pull ghcr.io/rmarshall31/kitronik_air_quality_control_hat_exporter:latest
```

```yaml
  kitronik-exporter:
    container_name: kitronik_exporter
    image: ghcr.io/rmarshall31/kitronik_air_quality_control_hat_exporter:latest
    restart: always
    ports:
      - 8000:8000
    volumes:
      - /dev/gpiomem:/dev/gpiomem
      - /dev/mem:/dev/mem
      - kitronik-data:/var/lib/kitronik
    privileged: true

volumes:
  kitronik-data:
```

`KITRONIK_DATA` (default `/var/lib/kitronik` in the image) is where the vendor
library writes `baselines.txt`. First boot without that file blocks ~5 minutes
on `calcBaselines()`. `/metrics` is bound before that so the process is
reachable; gauges appear after init.

The Dockerfile is `linux/arm64` only. A plain `docker build` on Docker Desktop
otherwise often produces amd64, which will not run on the Pi.

## Python / Pillow

Image base is `python:3.11-alpine`. Stay on 3.11: Kitronik's OLED code still
calls `font.getsize()`, removed in Pillow 10, and Pillow 9.x does not support
3.12+. Constraint is `Pillow>=9.2,<10`.

CI (GitHub Actions) lints and builds the arm64 image. It cannot exercise the
HAT; `RPi.GPIO` refuses to import off a Pi.
