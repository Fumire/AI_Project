FROM python:3

LABEL maintainer="230@fumire.moe"

ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update
RUN apt-get install -y g++ default-jdk ffmpeg libavcodec-extra

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache-dir pymysql konlpy nltk pydub gtts
ENTRYPOINT ["python", "run.py"]
