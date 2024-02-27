FROM python:3.11-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache make gcc musl-dev linux-headers

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "./exporter.py" ]