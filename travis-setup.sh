#!/bin/bash
set -x

cat <<EOF > tetra.conf
[sqlalchemy]
engine = postgres
host = tetra-db
port = 5432
username = postgres
password = password
database = tetra-db

[api]
default_limit = 25

[queue]
broker_url = amqp://tetra:password@tetra-queue:5672//
EOF

cat <<EOF > tetra-test.conf
[api]
base_url = http://localhost:7374
EOF

docker --version
docker-compose --version

make docker-build

make docker-db docker-queue
sleep 5
make docker-dev
sleep 5

make docker-port || true

docker-compose -f docker-compose.yml -f development.yml logs

