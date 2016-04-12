# tetra

`tetra` is a test result aggregator

# Using the makefile

Run a `make help` to see the makefile targets.

It contains a bunch of commands for managing a docker container for the
database. In non-linux places, it uses docker-machine to run docker in a vm.

To build and run the image/container

    $ make docker-build
    $ make docker-run

To see the ip and port of your postgres server:

    $ make docker-port

To get a postgres shell into the container:

    $ make docker-postgres-shell
