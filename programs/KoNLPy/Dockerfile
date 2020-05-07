FROM python:3

LABEL maintainer="230@fumire.moe"

ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update
RUN apt-get install -y g++ default-jdk

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache-dir gTTS pymysql konlpy nltk
RUN curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | /bin/bash
CMD ["/bin/bash"]
#ENTRYPOINT ["python", "run.py"]
