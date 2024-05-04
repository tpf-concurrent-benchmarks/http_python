FROM python:3.10-alpine

ARG N_WORKERS
ARG APP_HOST
ARG APP_PORT

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src src

CMD gunicorn src.main:app -b ${APP_HOST}:${APP_PORT} --workers ${N_WORKERS} -k uvicorn.workers.UvicornWorker