MAJOR:=$(shell bash -c 'source version.sh ; echo $$MAJOR')
BUILD:=$(shell bash -c 'source version.sh ; echo $$BUILD')
OS_NAME:=$(shell bash -c 'source version.sh ; echo $$OS_NAME')
ifeq "$(OS_NAME)" "win"
	PIP=$(shell pwd)/virtualenv/Scripts/pip
	VIRTUALENV_PKGS_DIR=$(shell pwd)/virtualenv/Lib/site-packages
else
	PIP=$(shell pwd)/virtualenv/bin/pip
	VIRTUALENV_PKGS_DIR=$(shell pwd)/virtualenv/lib/site-packages
endif
VIRTUALENV=$(shell which virtualenv)
PYTHON=$(shell which python)

PYTHON_FILES=setup.py mercy/version.py $(shell find mercy -iname "*py")
PYTHON_SDIST=./dist/mercy-$(MAJOR)-$(BUILD).tar.gz

.PHONY: clean
clean:
	rm -fr dist/*
	find mercy -iname "*pyc" -exec rm -vf \{\} \;
	cd puppet && make clean

############## Targets for puppet module

puppet/version.sh: version.sh
	cp version.sh $@

.PHONY: puppet
puppet: puppet_dist

.PHONY: puppet_dist
puppet_dist: puppet/version.sh
	cd puppet && make dist

.PHONY: puppet_install
puppet_install: puppet/version.sh
	cd puppet && make install

.PHONY: puppet_uninstall
puppet_uninstall: puppet/version.sh
	cd puppet && make uninstall

################ /puppet module

############### Targets for python app

dist: $(PYTHON_SDIST) puppet

sdist: $(PYTHON_SDIST)

mercy/version.py: version.sh
	source version.sh && echo "VERSION=\"$${MAJOR}-$${BUILD}\"" > $@

$(PYTHON_SDIST): $(PYTHON_FILES)
	$(PYTHON) setup.py sdist --formats=gztar

uninstall:
	rm -fr $(VIRTUALENV_PKGS_DIR)/mercy-* || echo 'not installed'

install: $(PYTHON_SDIST) virtualenv
	$(PIP) install $(PYTHON_SDIST) --upgrade

.PHONY: virtualenv
virtualenv:
	if [ ! -e $(PIP) ]; then \
		$(VIRTUALENV) --no-site-packages --distribute virtualenv ; \
	fi

################## /python app
