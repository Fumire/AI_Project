FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache-dir gtts pymysql nltk pydub
RUN python3 -m nltk.downloader all

RUN wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip -O /stanford-corenlp-full-2018-02-27.zip
RUN unzip /stanford-corenlp-full-2018-02-27.zip

ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update
RUN apt-get install -y g++ default-jdk espeak ffmpeg
#RUN java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000

#CMD ["/bin/bash"]
ENTRYPOINT ["python", "run.py"]
