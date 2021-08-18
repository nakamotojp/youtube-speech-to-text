FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY app/ /app

RUN apt-get update && \
  # ffmpegのインストールが必要
  apt-get -y install flac ffmpeg libavcodec-extra && \
  pip install --upgrade pip --no-cache-dir && \
  pip install -r requirements.txt --no-cache-dir
