.DEFAULT_GOAL := all
SHELL := /bin/bash

# Abort execution if there is NOT a virtual env
check_venv:
	@[ -n "$$VIRTUAL_ENV" ] || { printf "No venv activated.\nRun: 'source ./p_env.sh master'\n"; exit 1;}

# Abort execution if there is a virtual env 
check_deactivate:
	@[ -z "$$VIRTUAL_ENV" ] || { printf "❌ venv is active.\nRun: 'deactivate' before 'make clean'\n"; exit 1; }

openzepellin: check_venv
	echo "INSTALLING OPENZEPELLIN"
	npm init -y
	npm install @openzeppelin/contracts
	echo "OPENZEPELLIN INSTALLED"

all: check_venv openzepellin
	echo "base requirements done"

clean: check_deactivate
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf node_modules

re: clean all

.PHONY: check_venv check_deactivate openzepellin all clean re 