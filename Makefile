MAJOR:=$(shell bash -c 'source version.sh ; echo $$MAJOR')
BUILD:=$(shell bash -c 'source version.sh ; echo $$BUILD')
OS_NAME:=$(shell bash -c 'source version.sh ; echo $$OS_NAME')
ifeq "$(OS_NAME)" "win"
	PIP=$(shell pwd)/virtualenv/Scripts/pip
	SDIST_EXT=zip
	VIRTUALENV_PKGS_DIR=$(shell pwd)/virtualenv/Lib/site-packages
else
	PIP=$(shell pwd)/virtualenv/bin/pip
	SDIST_EXT=tar.gz
	VIRTUALENV_PKGS_DIR=$(shell pwd)/virtualenv/lib/site-packages
endif
VIRTUALENV=$(shell which virtualenv)
PYTHON=$(shell which python)

PYTHON_FILES=setup.py mercy/version.py $(shell find mercy -iname "*py")
PYTHON_SDIST=./dist/mercy-$(MAJOR)-$(BUILD).$(SDIST_EXT)

.PHONY: virtualenv
virtualenv:
	$(VIRTUALENV) --no-site-packages --distribute virtualenv

.PHONY: clean
clean:
	rm -fr dist/*
	find mercy -iname "*pyc" -exec rm -vf \{\} \;

sdist: $(PYTHON_SDIST)

mercy/version.py: version.sh
	source version.sh && echo "VERSION=\"$${MAJOR}-$${BUILD}\"" > $@

$(PYTHON_SDIST): $(PYTHON_FILES)
	$(PYTHON) setup.py sdist

uninstall:
	rm -fr $(VIRTUALENV_PKGS_DIR)/mercy-* || echo 'not installed'

install: $(PYTHON_SDIST)
	$(PIP) install $(PYTHON_SDIST) --upgrade
