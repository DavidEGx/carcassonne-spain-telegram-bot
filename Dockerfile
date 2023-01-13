FROM python:alpine3.17

COPY . /app
WORKDIR /app

ENV PYTHONPATH="/app:$PYTHONPATH"
RUN pip install -r requirements.txt

ENTRYPOINT /app/bin/telegram_bot
