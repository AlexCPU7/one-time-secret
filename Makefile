ENV_FILE = deploy/local/.env.local

# creates local .env files if they do not exist
ifeq ("$(wildcard $(ENV_FILE))","")
    $(eval s := $(shell cp deploy/local/.env.local.example ${ENV_FILE}))
endif

ifeq (generate,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  MESSAGES := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(MESSAGES):;@:)
endif

########

ENV_FILE = deploy/local/.env.local
NAME_APP = app
NAME_TEST = app-test

COMPOSE_YML ?= deploy/local/docker-compose.yml

MAIN = docker-compose --env-file ${ENV_FILE}

COMPOSE_MAIN = ${MAIN} -f ${COMPOSE_YML}
COMPOSE_TEST = docker-compose -p ${NAME_TEST} -f deploy/tests/docker-compose.yml

BASH_MAIN_COMMAND = ${MAIN} -f ${COMPOSE_YML} run --rm ${NAME_APP} /bin/bash -c

########

up:
	${COMPOSE_MAIN} up -d --build

test:
	${COMPOSE_TEST} run --rm ${NAME_TEST}


pip:
	${BASH_MAIN_COMMAND} "pip-compile requirements.in"

pip-list:
	$(BASH_MAIN_COMMAND) 'pip list'


generate:
	$(BASH_MAIN_COMMAND) 'alembic revision --autogenerate -m $(MESSAGES)'

migrate:
	$(BASH_MAIN_COMMAND) 'alembic upgrade head'

downgrade:
	$(BASH_MAIN_COMMAND) 'alembic downgrade -1'


build:
	${COMPOSE_MAIN} build --no-cache

start:
	${COMPOSE_MAIN} start

stop:
	${COMPOSE_MAIN} stop

down:
	${COMPOSE_MAIN} down
