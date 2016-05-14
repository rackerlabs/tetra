#!/bin/bash
set -x

cat <<EOF > tetra.conf
[sqlalchemy]
engine = postgres
host = 127.0.0.1
port = 5432
username = postgres
password = password
database = tetra-db

[api]
default_limit = 25

[queue]
broker_url = redis://localhost:6379/0
EOF

cat <<EOF > tetra-test.conf
[api]
base_url = http://localhost:7374
EOF

psql -c 'create database "tetra-db";' -U postgres
pip install -r requirements.txt
# required to use redis with celery
pip install -U celery[redis]

# the effect of this is we see our print statements printed immediately
export PYTHONUNBUFFERED=1
gunicorn --daemon -t 120 --bind 127.0.0.1:7374 tetra.app:application
celery --detach --app=tetra.worker.app worker --loglevel=INFO
