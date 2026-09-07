# Kitronik Air Quality Control HAT Prometheus Exporter

```bash
docker build -t kitronik_exporter .
docker run --privileged \
  -v /dev/gpiomem:/dev/gpiomem \
  -v /dev/mem:/dev/mem \
  -v kitronik-data:/var/lib/kitronik \
  -p 8000:8000 kitronik_exporter
```

Alternatively:
```bash
docker pull rmarshall31/kitronik_exporter:latest
```

with docker-compose
```yaml
  kitronik-exporter:
    container_name: kitronik_exporter
    image: kitronik_exporter:latest
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

AQI & colors: https://www.airnow.gov/aqi/aqi-basics/
