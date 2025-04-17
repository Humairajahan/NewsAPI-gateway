FROM python:latest

WORKDIR /codebase

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip3 install --upgrade pip

COPY requirements.txt /codebase/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src /codebase/src