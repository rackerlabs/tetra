FROM python:2.7

WORKDIR /tetra/
ADD requirements.txt /tetra/requirements.txt
RUN pip install -r requirements.txt
ADD . /tetra
RUN adduser --disabled-password --gecos '' tetra-worker
