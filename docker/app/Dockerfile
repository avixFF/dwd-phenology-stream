FROM python:3.8
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-mysql-client

RUN pip install --no-cache-dir \
    matplotlib \
    pandas \
    requests \
    pydash \
    bs4 \
    python-dotenv \
    peewee \
    pymysql

COPY . .

CMD while true; do ./run.sh; sleep 600; done
