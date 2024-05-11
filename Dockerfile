FROM python:latest

LABEL Maintainer="stepan"

COPY requirements.txt /home/
WORKDIR /home

COPY main.py ./
COPY settings.py ./
COPY confirmationSettings.py ./
COPY utils.py ./

RUN mkdir ./media_from_dialogs
RUN mkdir ./logs
RUN pip install -r /home/requirements.txt

CMD [ "python", "./main.py"]