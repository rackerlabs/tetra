# tetra

`tetra` is a test result aggregator

# Using the makefile

The makefile contains a bunch of commands for managing a docker containers for
all of tetra's services. You will need `docker-compose` installed. In non-linux
places, it uses `docker-machine` to run docker containers in a linux vm.

First, run a `make help` to see the makefile targets.

To build the containers:

    $ make docker-build

To build/run the containers:

    $ make docker-dev

_Note: The db and queue take several seconds to start up. You may get errors in
the api and worker on the first start up becuase of this. Restarting the api
and worker should fix this._

To see the `<ip>:<port>` of different services:

    $ make docker-port

To get a postgres shell in the container:

    $ make docker-postgres-shell


# Configuring tetra

Tetra reads all of its config from a `tetra.conf` file. The complete list of
options is in `tetra/config.py`. Here's an example `tetra.conf` file:

    [sqlalchemy]
    engine = postgres
    host = localhost
    port = 5432
    username = postgres
    password = password
    database = tetra-db

    [api]
    default_limit = 25

    [queue]
    broker_url = amqp://tetra:password@localhost:5672//

Tip: When using the docker dev environment, you can use the names of the
services in the `docker-compose.yml` as hostnames:

    host = db
    ...
    broker_url = amqp://tetra:password@queue:5672//

# Running the tests

The tests look for a `tetra-test.conf` file. The complete list of options is in
`tests/config.py`. Here's an example `tetra-test.conf` file:

    [api]
    base_url = http://localhost:7374

The you can either use `tox` to run the tests:

    tox -e functional

Or you can use the makefile:

    $ pip install -r test-requirements.txt
    $ make test
