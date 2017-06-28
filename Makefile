

SHELL = /bin/sh

ROOT=$(shell pwd)/py

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
