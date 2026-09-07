FROM python:3.11-alpine AS builder

WORKDIR /build

RUN apk add --no-cache make gcc musl-dev linux-headers

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY exporter.py .

ENV KITRONIK_DATA=/var/lib/kitronik
VOLUME /var/lib/kitronik

EXPOSE 8000

CMD ["python", "./exporter.py"]
