FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache-dir pymysql deepspeech

#ENTRYPOINT ["python", "run.py"]
CMD ["/bin/bash"]
