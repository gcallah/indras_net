FROM python:3.6.0

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENV user_type TERMINAL
ENV PYTHONPATH "/home/IndrasNet:${PYTHONPATH}"

WORKDIR /home/IndrasNet/
