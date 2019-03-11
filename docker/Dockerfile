FROM python:3.6.0

COPY requirements.txt /requirements.txt
COPY requirements-dev.txt /requirements-dev.txt

RUN pip install --upgrade pip

RUN pip install -r requirements-dev.txt

ENV user_type TERMINAL
ENV PYTHONPATH "/home/IndrasNet:${PYTHONPATH}"

WORKDIR /home/IndrasNet/
