.PHONY: all install-dev lint test coverage cov test-all tox clean-pyc

all: test

install-dev: clean
	pip install -q -e .[dev]

lint: clean-pyc
	pylint lightnode tests

test: clean-pyc install-dev
	pytest

coverage: clean-pyc install-dev
	coverage run -m pytest
	coverage report -m

test-all: install-dev
	tox

sdist: clean
	python setup.py sdist bdist_wheel
	ls -lh dist

upload-pypi: sdist
	twine upload dist/* --repository pypi --verbose

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -rf .coverage .pytest_cache

clean-pyc:
	@echo "clean pyc"
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
