FROM python:3.6.0

COPY requirements.txt /requirements.txt
COPY requirements-dev.txt /requirements-dev.txt

RUN pip install --upgrade pip

RUN pip install -r requirements-dev.txt

ENV project IndrasNet
ENV user_type TERMINAL
ENV PYTHONPATH "/home/${project}:${PYTHONPATH}"
ENV props_dir "/home/${project}/APIServer/data/"
ENV FLASK_ENV development
ENV INDRA_HOME /home/${project}

WORKDIR /home/$project/
