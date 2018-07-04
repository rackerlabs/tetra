FROM python:2.7

WORKDIR /tetra/
ADD . /tetra
RUN pip install .
RUN pip install gunicorn
RUN adduser --disabled-password --gecos '' tetra-worker
