.PHONY: docs deploy-docs test start
SHELL := /bin/bash

# used to check what platform we're on, to see if we should use a vm for docker
UNAME := $(shell uname)

# the image and container are both named this
DOCKER_TAG := tetra-api
DOCKER_WORKER_TAG := tetra-worker
DOCKER_DB_TAG := tetra-db
DOCKER_QUEUE_TAG := tetra-queue
DOCKER_UI_TAG := tetra-ui

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
	@echo 'Commands:'
	@echo '  start                      - start the tetra api, running locally'
	@echo '  test                       - run tests (you must first write tetra-test.conf)'
	@echo '  rabbitmq-admin-ui          - open the rabbitmq management interface in a browser'
	@echo '  docs                       - build the docs and start a local server to view them'
	@echo '  deploy-docs                - build and deploy docs to github pages'
	@echo 'Docker commands:'
	@echo '  docker-build               - build all docker images for a dev environment'
	@echo '  docker-dev                 - build/run all images/containers for a dev environment'
	@echo '  docker-restart-worker      - restart the worker container'
	@echo '  docker-db                  - run the postgres docker container in background ($(DOCKER_DB_TAG))'
	@echo '  docker-queue               - run the rabbitmq docker container in background ($(DOCKER_QUEUE_TAG))'
	@echo '  docker-logs                - follow the logs from all containers'
	@echo '  docker-ps                  - list running docker containers'
	@echo '  docker-stop                - stop the containers'
	@echo '  docker-down                - stop and remove the containers'
	@echo '  docker-port                - display the real <ip>:<port> for different containers'
	@echo '  docker-machine-create      - start the boot2docker vm ($(DOCKER_MACHINE_NAME))'
	@echo '                               NOTE: this is a no-op on linux.'
	@echo '  docker-machine-rm          - remove the boot2docker vm ($(DOCKER_MACHINE_NAME))'
	@echo '                               NOTE: this is a no-op on linux.'
	@echo '  docker-env                 - use "eval $$(make docker-env)"' to set
	@echo '                               docker vars for the boot2docker vm'
	@echo '                               NOTE: this is a no-op on linux.'
	@echo '  docker-postgres-shell      - start the postgres shell in your container'

start:
	gunicorn --reload -t 120 --bind 127.0.0.1:7374 tetra.app:application

test:
	py.test -v ./tests

docs:
	mkdocs serve

# running with tox resulted in "Unknown committed ..." on the gh-pgaes branch
deploy-docs:
	mkdocs gh-deploy -c

docker-build: docker-machine-create
	$(WITH_DOCKER_ENV) && docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

docker-dev:
	$(WITH_DOCKER_ENV) && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up api worker ui

docker-restart-worker:
	$(WITH_DOCKER_ENV) && docker-compose -f docker-compose.yml -f docker-compose.dev.yml restart worker

docker-db:
	$(WITH_DOCKER_ENV) && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d db

docker-queue:
	$(WITH_DOCKER_ENV) && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d queue

docker-logs:
	$(WITH_DOCKER_ENV) && docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

docker-ps:
	$(WITH_DOCKER_ENV) && docker ps

docker-stop:
	$(WITH_DOCKER_ENV) && docker-compose stop

docker-down:
	$(WITH_DOCKER_ENV) && docker-compose down

docker-port:
ifeq ($(UNAME), Linux)
	@echo API=$(shell $(WITH_DOCKER_ENV) && docker port $(DOCKER_TAG) 7374)
	@echo DB=$(shell $(WITH_DOCKER_ENV) && docker port $(DOCKER_DB_TAG) 5432)
	@echo QUEUE=$(shell $(WITH_DOCKER_ENV) && docker port $(DOCKER_QUEUE_TAG) 5672)
	@echo UI=$(shell $(WITH_DOCKER_ENV) && docker port $(DOCKER_UI_TAG) 80)
else
	@echo API=`docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		$(WITH_DOCKER_ENV) && docker port $(DOCKER_TAG) 7374 | cut -d':' -f 2 \
	)
	@echo DB=`docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		$(WITH_DOCKER_ENV) && docker port $(DOCKER_DB_TAG) 5432 | cut -d':' -f 2 \
	)
	@echo QUEUE=`docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		$(WITH_DOCKER_ENV) && docker port $(DOCKER_QUEUE_TAG) 5672 | cut -d':' -f 2 \
	)
	@echo UI=`docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		$(WITH_DOCKER_ENV) && docker port $(DOCKER_UI_TAG) 80 | cut -d':' -f 2 \
	)
endif

docker-postgres-shell:
	$(WITH_DOCKER_ENV) && docker exec -it $(DOCKER_DB_TAG) \
		bash -c 'PGPASSWORD=password psql -U postgres'

rabbitmq-admin-ui:
	@echo "To login, check docker-compose.yml for RABBITMQ_DEFAULT_USER and RABBITMQ_DEFAULT_PASS"
ifeq ($(UNAME), Linux)
	xdg-open http://`docker port $(DOCKER_QUEUE_TAG) 15672`
else
	open http://`docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		$(WITH_DOCKER_ENV) && docker port $(DOCKER_QUEUE_TAG) 15672 | cut -d':' -f 2 \
	)
endif

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
