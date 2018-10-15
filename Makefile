.PHONY: clean-pyc clean-build docs clean

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "watch - run code coverage whenever a file changes with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

format:
	black rich_text_renderer tests

lint:
	flake8 rich_text_renderer

test:
	python setup.py test

test-all:
	tox

coverage: format lint
	coverage run --source rich_text_renderer setup.py test
	coverage report -m

watch:
	fswatch -d -e rich_text_renderer/__pycache__ -e tests/__pycache__ rich_text_renderer tests | xargs -n1 make coverage

docs:
	rm -f _docs/rich_text_renderer.rst
	rm -f _docs/modules.rst
	rm -rf _docs/_build/*
	sphinx-apidoc -o _docs/ rich_text_renderer
	cd _docs && make html
	cp LICENSE _docs/_build/html/
	rm -rf docs
	cp -r _docs/_build/html docs
	open docs/index.html

git-docs: docs
	git add docs
	git commit --amend -C HEAD

# TODO: Add git-docs step once Sphinx docs are set up.
release: clean
	python setup.py publish

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
