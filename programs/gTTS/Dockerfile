FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache gTTS pymysql
ENTRYPOINT ["python", "run.py"]
