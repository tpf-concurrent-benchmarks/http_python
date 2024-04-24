FROM python:3.10-alpine

ENV HOST=0.0.0.0
ENV PORT=80

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src src

CMD uvicorn src.main:app --host $HOST --port $PORT