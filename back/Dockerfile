FROM python:3.12-slim-bullseye
WORKDIR /proto_app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        default-libmysqlclient-dev \
        pkg-config \
        build-essential \
        libpython3-dev \
        libpq-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./wait-for-it.sh .

COPY . .

EXPOSE 5000