# tetra

Running tests on a regular basis will inevitably reveal some that are "flakey."
That is, sometimes, they fail inexplicably, and then start running normally again shortly thereafter.
Sifting through the failures manually would consume too much time.

`tetra` is a test result aggregator.
It's still a proof of concept side project, with lots to improve.
However, the core idea is simple:
we want a tool that lets testers store results in a consistent format,
and which makes historical results available through a RESTful API
so tools and dashboards can analyze results easier and faster.

`tetra` looks for certain key strings in XUnit-style test results, aggregating what it finds along the way.
As long as your testing infrastructure is capable of yielding XUnit-compatible output,
`tetra` should be able to consume the data.

Please note that `tetra` is, at present, a part-time project. 
However, contributions are welcome.

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


# Configuring `tetra`

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

# Running `tetra`'s tests

The tests look for a `tetra-test.conf` file. The complete list of options is in
`tests/config.py`. Here's an example `tetra-test.conf` file:

    [api]
    base_url = http://localhost:7374

The you can either use `tox` to run the tests:

    tox -e functional

Or you can use the makefile:

    $ pip install -r test-requirements.txt
    $ make test
