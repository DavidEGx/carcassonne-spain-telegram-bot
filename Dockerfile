FROM python:alpine3.14

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT /app/bin/bot
