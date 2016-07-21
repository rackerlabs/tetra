FROM python:2.7

WORKDIR /tetra/
ADD requirements.txt /tetra/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main 9.5" > /etc/apt/sources.list.d/pgdg.list
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add -
RUN apt-get update
RUN apt-get install postgresql-client -y
ADD . /tetra
RUN adduser --disabled-password --gecos '' tetra-worker
