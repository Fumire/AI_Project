FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN apt-get update
RUN apt-get install -y libsndfile1 espeak

RUN pip install --no-cache-dir pymysql numpy torch librosa Unidecode tensorboard tensorboardX scipy tqdm soundfile phonemizer bokeh

COPY TTS/setup.py /setup.py
RUN python setup.py install

ENV LANG C.UTF-8

#ENTRYPOINT ["python", "run.py"]
CMD ["/bin/bash"]
