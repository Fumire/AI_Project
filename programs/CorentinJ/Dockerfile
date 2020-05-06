FROM python:3

LABEL maintainer="230@fumire.moe"

EXPOSE 3306

WORKDIR /script
VOLUME /data

RUN pip install --no-cache-dir tensorflow numpy scipy Unidecode torch

CMD ["/bin/bash"]
#ENTRYPOINT ["python", "run.py"]
