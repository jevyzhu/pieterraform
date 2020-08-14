#!/usr/bin/make

PYTHON_VER := 3.8
PROJECT := pieterraform
DEV_USER := dev
DEV_CONTAINER := ${PROJECT}-devenv
DEV_SRV := ${PROJECT}-dev-env-srv 

SHELL = /bin/bash

CURRENT_USER_ID := $(shell id -u ${USER}) 
CURRENT_GROUP_ID := $(shell id -g ${USER}) 

.PHONY: clean test dist dist-upload docker-dev pretty autopep8

define dev-docker =
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	PYTHON_VER=${PYTHON_VER} \
	docker-compose up -d --build ${DEV_SRV}
endef


dist: clean test
	if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER} \
		/bin/bash -c 'rm -rf dist/* && python setup.py sdist && python setup.py bdist_wheel' \
	;else \
		python setup.py sdist &&\
		python setup.py bdist_wheel \
	;fi

test:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER} \
		pytest \
			--cov=${PROJECT} \
			--cov-report=term \
			--cov-report=html:coverage-report \
			-v tests \
	;else \
		pytest \
			--cov=${PROJECT} \
			--cov-report=term \
			--cov-report=html:coverage-report \
			-v tests \
	;fi

dist-upload:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec -it ${DEV_CONTAINER}  \
			twine upload dist/* \
	;else \
		twine upload dist/* \
	;fi

docker-dev:
	$(dev-docker)


clean:
	@find . -name '*.py[co]' -delete
	@find . -name '__pycache__' -delete
	@rm -fr dist build *egg*info* coverage* .coverage

pretty:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER}  \
		yapf -i -r  .  > /dev/null 2>&1 ||: \
	;else \
		yapf -i -r  .  > /dev/null 2>&1 ||: \
	;fi

autopep8:
	@if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(dev-docker) > /dev/null &&\
		docker exec ${DEV_CONTAINER}  \
		/bin/bash -c " find . -name '*.py' | xargs autopep8 --in-place --aggressive " \
	;else \
		find . -name '*.py' | xargs autopep8 --in-place --aggressive  \
	;fi
