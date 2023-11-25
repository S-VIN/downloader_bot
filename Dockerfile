FROM python:latest

LABEL Maintainer="stepan"

COPY requirements.txt /home/
WORKDIR /home

COPY main.py ./
COPY peer.py ./
COPY settings.py ./

RUN mkdir ./media_from_dialogs
RUN mkdir ./logs
RUN pip install -r /home/requirements.txt

# CMD [ "python", "./main.py"]