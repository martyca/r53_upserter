FROM python:alpine

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG A_RECORD

WORKDIR /main

COPY main.py /main
COPY requirements.txt /main

RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]

ENTRYPOINT ["python", "main.py"]