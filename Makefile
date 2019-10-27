.PHONY: setup activate populate process visualize send

SHELL := /bin/bash

help:
	@echo "setup - Setup the repository"
	@echo "activate - Performing activation for SaltEdge Account"
	@echo "populate - Downloading Raw Dataset from the SaltEdge Account"
	@echo "process - Processing the Downloaded Transactional Dataset"
	@echo "visualize - Perfomring Visualization of the Transformed Dataset"
	@echo "send - Sending the Visualization on the target email"

setup:
	bash bin/setup.sh

activate:
	export PYTHONPATH=${PWD} && pipenv run python src/activate.py

populate:
	export PYTHONPATH=${PWD} && pipenv run python src/populate.py --year=${YEAR} --month=${MONTH}

process:
	export PYTHONPATH=${PWD} && pipenv run python src/process.py --year=${YEAR} --month=${MONTH}

send:
	export PYTHONPATH=${PWD} && pipenv run python src/send.py --year=${YEAR} --month=${MONTH} --email=${EMAIL}

visualize:
	export PYTHONPATH=${PWD} && pipenv run python src/visualize.py --year=${YEAR} --month=${MONTH}