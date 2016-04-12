# tetra

`tetra` is a test result aggregator

# Using the makefile

The makefile contains a bunch of commands for managing a docker container for
the database. In non-linux places, it uses docker-machine to run docker in a
vm.

Run a `make help` to see the makefile targets.

To build and run the image/container

    $ make docker-build
    $ make docker-run

To see the ip and port of your postgres server:

    $ make docker-port

To get a postgres shell in the container:

    $ make docker-postgres-shell
