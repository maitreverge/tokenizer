.DEFAULT_GOAL := all

openzepellin:
	@echo "INSTALLING OPENZEPELLIN"
	npm init -y
	npm install @openzeppelin/contracts
	@echo "OPENZEPELLIN INSTALLED"
	@echo "base requirements done"

all: openzepellin
	@echo "Now run 'source ./p_env.sh master' for finishing installation"

clean:
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf node_modules

re: clean all

.PHONY: openzepellin all clean re