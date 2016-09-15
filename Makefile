.PHONY: docs deploy-docs test start
SHELL := /bin/bash

# used to check what platform we're on, to see if we should use a vm for docker
UNAME := $(shell uname)
# try xdg-open on linux
OPEN := open

# the image and container are both named this
DOCKER_TAG := tetra-api
DOCKER_WORKER_TAG := tetra-worker
DOCKER_DB_TAG := tetra-db
DOCKER_QUEUE_TAG := tetra-queue
DOCKER_UI_TAG := tetra-ui

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

docker-build:
	docker-compose -f docker-compose.yml -f development.yml build

docker-dev:
	docker-compose -f docker-compose.yml -f development.yml up -d api worker ui

docker-deploy-production:
	docker-compose -f docker-compose.yml -f production.yml up -d

docker-restart-worker:
	docker-compose -f docker-compose.yml -f development.yml restart worker

docker-db:
	docker-compose -f docker-compose.yml -f development.yml up -d db

docker-queue:
	docker-compose -f docker-compose.yml -f development.yml up -d queue

docker-logs:
	docker-compose -f docker-compose.yml -f development.yml logs -f

docker-ps:
	docker ps

docker-stop:
	docker-compose stop

docker-down:
	docker-compose down

docker-port:
	@echo API=$(shell docker port $(DOCKER_TAG) 7374)
	@echo DB=$(shell docker port $(DOCKER_DB_TAG) 5432)
	@echo QUEUE=$(shell docker port $(DOCKER_QUEUE_TAG) 5672)
	@echo UI=$(shell docker port $(DOCKER_UI_TAG) 80)

docker-postgres-shell:
	docker exec -it $(DOCKER_DB_TAG) \
		bash -c 'PGPASSWORD=password psql -U postgres'

rabbitmq-admin-ui:
	@echo "To login, check docker-compose.yml for RABBITMQ_DEFAULT_USER and RABBITMQ_DEFAULT_PASS"
	open http://`docker-machine ip $(DOCKER_MACHINE_NAME)`:$(shell \
		docker port $(DOCKER_QUEUE_TAG) 15672 | cut -d':' -f 2 \
	)
