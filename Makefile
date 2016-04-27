SHELL := /bin/bash

# used to check what platform we're on, to see if we should use a vm for docker
UNAME := $(shell uname)

# the image and container are both named this
DOCKER_TAG := tetra-db

# set some variables for docker-machine, which we need outside of Linux
ifeq ($(UNAME), Linux)
	# 0n Linux, these variables are set to be no-ops
	DOCKER_MACHINE_NAME := "<n/a>"
	DOCKER_MACHINE_CHECK_NAME := $(DOCKER_MACHINE_NAME)
	WITH_DOCKER_ENV := true
else
	DOCKER_MACHINE_NAME := tetra-docker-vm
	DOCKER_MACHINE_CHECK_NAME := $(shell docker-machine ls --filter name=$(DOCKER_MACHINE_NAME) | tail -n 1 | cut -d' ' -f 1)
	WITH_DOCKER_ENV := eval `docker-machine env $(DOCKER_MACHINE_NAME)`
endif

help:
	@echo 'Api commands:'
	@echo '  start                      - start the tetra api, running locally'
	@echo 'Docker commands:'
	@echo '  docker-build               - build the postgres docker image ($(DOCKER_TAG))'
	@echo '  docker-run                 - run the postgres docker container ($(DOCKER_TAG))'
	@echo '  docker-ps                  - list running docker containers'
	@echo '  docker-stop                - stop and rm the container ($(DOCKER_TAG))'
	@echo '  docker-port                - display the real <ip>:<port> for the database'
	@echo '  docker-machine-create      - start the boot2docker vm ($(DOCKER_MACHINE_NAME))'
	@echo '                               NOTE: this is a no-op on linux.'
	@echo '  docker-machine-rm          - remove the boot2docker vm ($(DOCKER_MACHINE_NAME))'
	@echo '                               NOTE: this is a no-op on linux.'
	@echo '  docker-env                 - use "eval $$(make docker-env)"' to set
	@echo '                               docker vars for the boot2docker vm'
	@echo '                               NOTE: this is a no-op on linux.'
	@echo '  docker-postgres-shell      - start the postgres shell in your container'

start:
	gunicorn --reload --bind 127.0.0.1:7374 tetra.app:application

test:
	py.test -v ./tests

docker-build: docker-machine-create
	$(WITH_DOCKER_ENV) && docker build -t $(DOCKER_TAG) .

docker-run:
	$(WITH_DOCKER_ENV) && docker run -p 5432 -d --name $(DOCKER_TAG) $(DOCKER_TAG)

docker-ps:
	$(WITH_DOCKER_ENV) && docker ps

docker-stop:
	$(WITH_DOCKER_ENV) && docker stop $(DOCKER_TAG) && docker rm $(DOCKER_TAG)

docker-port:
ifeq ($(UNAME), Linux)
	$(WITH_DOCKER_ENV) && docker port $(DOCKER_TAG) 5432
else
	@echo `docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		$(WITH_DOCKER_ENV) && docker port $(DOCKER_TAG) 5432 | cut -d':' -f 2 \
	)
endif

docker-postgres-shell:
	$(WITH_DOCKER_ENV) && docker exec -it $(DOCKER_TAG) \
		bash -c 'PGPASSWORD=password psql -U postgres'

docker-machine-create:
ifneq ($(DOCKER_MACHINE_CHECK_NAME), $(DOCKER_MACHINE_NAME))
	docker-machine create --driver virtualbox $(DOCKER_MACHINE_NAME)
endif

docker-machine-rm:
ifneq ($(UNAME), Linux)
	docker-machine rm $(DOCKER_MACHINE_NAME)
endif

docker-env:
ifneq ($(UNAME), Linux)
	@docker-machine env $(DOCKER_MACHINE_NAME)
endif
