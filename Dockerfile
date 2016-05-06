FROM python:2.7

WORKDIR /tetra/
ADD requirements.txt /tetra/requirements.txt
RUN pip install -r requirements.txt
ADD . /tetra
EXPOSE 7374
CMD gunicorn --reload -t 120 --bind 0.0.0.0:7374 tetra.app:application
