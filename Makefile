#!/usr/bin/make
PROJECT := pieterraform
DEV_CONTAINER := ${PROJECT}-devenv
DEV_USER := hacker

SHELL = /bin/bash

CURRENT_USER_ID := $(shell id -u ${USER}) 
CURRENT_GROUP_ID := $(shell id -g ${USER}) 

.PHONY: clean start-dev-docker test dist dist-upload 

define start-docker =
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	docker-compose up -d --build
endef

define start-pytest =
	pytest \
		--cov=${PROJECT} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		-v tests
endef

start-dev-docker:
	if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(start-docker) \
	;fi

clean:
	find . -name '*.py[co]' -delete
	rm -rf dist/* 
	rm -fr build/*

test: start-dev-docker
	if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(start-docker) &&\
		docker exec -w /home/${DEV_USER}/${PROJECT} ${DEV_CONTAINER} \
		$(start-pytest) \
	;else \
		$(start-pytest) \
	;fi


dist: clean start-dev-docker
	if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(start-docker) &&\
		docker exec -w /home/${DEV_USER}/${PROJECT} ${DEV_CONTAINER} bash -c \
		'python setup.py sdist && python setup.py bdist_wheel'  \
	;else \
		python setup.py sdist &&\
		python setup.py bdist_wheel \
	;fi

dist-upload: start-dev-docker
	if [[ -z "${IN_DEV_DOCKER}" ]]; then \
		$(start-docker) &&\
		docker exec -it -w /home/${DEV_USER}/${PROJECT} ${DEV_CONTAINER}  \
			twine upload dist/* \
	;else \
		twine upload dist/* \
	;fi
