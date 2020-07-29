#!/usr/bin/make
PROJECT := pyrraform
DEV_CONTAINER := ${PROJECT}-devenv
DEV_USER := hacker

SHELL = /bin/bash

CURRENT_USER_ID := $(shell id -u ${USER}) 
CURRENT_GROUP_ID := $(shell id -g ${USER}) 

.PHONY: clean start-dev-docker test-docker test dist dist-upload dist-upload-docker

start-dev-docker:
	env CURRENT_USER_ID=${CURRENT_USER_ID} \
	CURRENT_GROUP_ID=${CURRENT_GROUP_ID} \
	CURRENT_PROJECT=${PROJECT} \
	DEV_USER=${DEV_USER} \
	docker-compose up -d --build

clean:
	find . -name '*.py[co]' -delete

test: 
	pytest \
		--cov=${PROJECT} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		-v tests

test-docker: start-dev-docker
	docker exec -w /home/${DEV_USER}/${PROJECT} ${DEV_CONTAINER}  \
	pytest \
		--cov=${PROJECT} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		-v tests


dist: clean
	rm -rf dist/* 
	python setup.py sdist
	python setup.py bdist_wheel

dist-docker: clean
	docker exec -w /home/${DEV_USER}/${PROJECT} ${DEV_CONTAINER} \
	/bin/bash -c 'rm -rf dist/* &&  python setup.py sdist &&  python setup.py bdist_wheel'

dist-upload:
	twine upload dist/*

dist-upload-docker:
	docker exec -it -w /home/${DEV_USER}/${PROJECT} ${DEV_CONTAINER}  \
	twine upload dist/*
