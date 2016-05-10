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
EOF

cat <<EOF > tetra-test.conf
[api]
base_url = http://localhost:7374
EOF

pip install -r requirements.txt
