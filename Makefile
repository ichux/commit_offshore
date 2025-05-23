# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help: Commit Offshore Makefile help
# help:

SHELL := /bin/bash

.PHONY: help
# help: help				- Please use "make <target>" where <target> is one of
help:
	@grep "^# help\:" Makefile | sed 's/\# help\: //' | sed 's/\# help\://'

.PHONY: e
# help: e				- copy env
e:
	@cp env.example .env

.PHONY: b
# help: b				- build containers
b:
	@COMPOSE_BAKE=true BUILDKIT_PROGRESS=plain docker compose -f docker-compose.yml up --build -d

.PHONY: ts
# help: ts				- run tests
ts:
	@docker exec -i cf_offshore_manager pytest -v

.PHONY: gd
# help: gd				- generate faker data
gd:
	@docker exec -i cf_offshore_manager python3 generate_data.py

.PHONY: ai
# help: ai				- autogenerate files e.g. make ai i=initial_migration, make ai i='Value point'
ai:
	@docker exec -i cf_offshore_manager alembic revision --autogenerate -m "$(i)" || printf ''

.PHONY: uh
# help: uh				- alembic upgrade head
uh:
	@docker exec -i cf_offshore_manager alembic upgrade head

.PHONY: uhs
# help: uhs				- show sql for alembic upgrade head
uhs:
	@docker exec -i cf_offshore_manager alembic upgrade head --sql

.PHONY: ac
# help: ac				- alembic current
ac:
	@docker exec -i cf_offshore_manager alembic current

.PHONY: ah
# help: ah				- alembic history
ah:
	@docker exec -i cf_offshore_manager alembic history

.PHONY: tests
# help: tests				- run pytest
tests:
	@pytest -s tests

.PHONY: fr
# help: fr				- pip freeze
fr:
	@pip freeze | grep -v 'wheel\|setuptools' > containers/requirements.txt
