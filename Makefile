

SHELL = /bin/sh

ROOT=$(shell pwd)/py
TESTENV=${ROOT}/.test-env
DIST=${ROOT}/dist/

.PHONY: two
two: $(ROOT)/.py2-env
.PHONY: three
three: $(ROOT)/.py3-env
.PHONY: freeze
freeze:
	cd $(ROOT) && pipenv lock
.PHONY: test test-two test-three
test: test-two test-three
test-two: two
	cd $(ROOT) && pipenv run unit2 discover
test-three: three
	cd $(ROOT) && pipenv run unit2 discover

clean:
	- rm $(ROOT)/.py3-env
	- rm $(ROOT)/.py2-env

.PHONY: publish
publish: test test-package build
	- twine upload $(DIST)/*py3*
	- twine upload $(DIST)/*py2*

.PHONY: build build-two build-three
build: build-two build-three
build-two: two
	cd $(ROOT) && pipenv run python setup.py bdist_wheel
build-three: three
	cd $(ROOT) && pipenv run python setup.py bdist_wheel

.PHONY: package
package: build $(TESTENV)
	source '${TESTENV}'/bin/activate && python
.PHONY: test-package
test-package: build $(TESTENV)
	source '${TESTENV}'/bin/activate && unit2 discover -v

$(DIST):
	mkdir -p $(DIST)

$(TESTENV): build-three
	virtualenv $(TESTENV) --python=python3
	source '${TESTENV}'/bin/activate && pip install $(DIST)/*py3* unittest2


$(ROOT)/.py2-env: $(ROOT)/Pipfile $(ROOT)/Pipfile.lock
	- rm $(ROOT)/.py3-env
	cd $(ROOT) && pipenv --two install -d
	touch "$@"

$(ROOT)/.py3-env: $(ROOT)/Pipfile $(ROOT)/Pipfile.lock
	- rm $(ROOT)/.py2-env
	cd $(ROOT) && pipenv --three install -d
	touch "$@"

$(ROOT)/Pipfile:
	cd $(ROOT) && pipenv check

$(ROOT)/Pipfile.lock: $(ROOT)/Pipfile
	cd $(ROOT) && pipenv lock
