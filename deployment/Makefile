# Make shit run in the same shell instead of different shells

SHELL := /bin/bash
.ONESHELL:

# 	Check if the current makefile does run in a python venv
check_venv:
	@if [[ -z "$${VIRTUAL_ENV}" ]]; then\
			echo "No venv acivated";\
			exit;\
	fi
	echo "VENV ACTIVATED"
# 	source ./p_env.sh master
# 	bash -c "source ./.venv/bin/activate"

openzepellin: check_venv
	echo "INSTALLING OPENZEPELLIN"
	npm init -y
	npm install @openzeppelin/contracts
	echo "OPENZEPELLIN INSTALLED"

all: venv openzepellin
	echo "base requirements done"


clean:
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf node_modules



re: clean all

# Prune does removes volumes, including the DB.
prune:
	docker system prune --all --volumes --force

.PHONY: venv