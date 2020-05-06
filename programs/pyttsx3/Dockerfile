FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache pymysql pyttsx3 pydub

RUN apt-get update
RUN apt-get install -y espeak ffmpeg

#ENTRYPOINT ["python", "run.py"]
CMD ["/bin/bash"]
