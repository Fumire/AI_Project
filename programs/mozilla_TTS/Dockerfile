FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306
EXPOSE 5002

WORKDIR /script
VOLUME /data

RUN apt-get update
RUN apt-get install -y libsndfile1 espeak

COPY TTS/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

ENV LANG C.UTF-8

#ENTRYPOINT ["python", "run.py"]
CMD ["/bin/bash"]
