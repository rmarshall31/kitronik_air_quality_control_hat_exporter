FROM python:3.11-alpine AS builder

ARG TARGETARCH
RUN if [ "$TARGETARCH" != "arm64" ]; then \
        echo "linux/arm64 only, got TARGETARCH=$TARGETARCH" >&2; \
        exit 1; \
    fi

WORKDIR /build

RUN apk add --no-cache make gcc musl-dev linux-headers

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

WORKDIR /usr/src/app

LABEL org.opencontainers.image.source="https://github.com/rmarshall31/kitronik_air_quality_control_hat_exporter"
LABEL org.opencontainers.image.description="Prometheus exporter for the Kitronik Air Quality Control HAT"
LABEL org.opencontainers.image.licenses="MIT"

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY exporter.py .

ENV KITRONIK_DATA=/var/lib/kitronik
VOLUME /var/lib/kitronik

EXPOSE 8000

CMD ["python", "./exporter.py"]
