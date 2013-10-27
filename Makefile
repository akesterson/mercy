MAJOR:=$(shell bash -c 'source version.sh ; echo $$MAJOR')
BUILD:=$(shell bash -c 'source version.sh ; echo $$BUILD')
OS_NAME:=$(shell bash -c 'source version.sh ; echo $$OS_NAME')
PIP=$(shell pwd)/virtualenv/bin/pip
VIRTUALENV_PKGS_DIR=$(shell pwd)/virtualenv/lib/python2.7/site-packages
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
	bash -c 'source version.sh && echo "VERSION=\"$${MAJOR}-$${BUILD}\"" > $@'

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

################## Targets for supporting development work

databases: databases/fda_ndc.zip  databases/drugbank.xml.zip

.PHONY: databases/fda_ndc.zip
databases/fda_ndc.zip:
	rm -fr databases/fda_ndc*
	mkdir -p databases/fda_ndc
	rm -f fda_ndc.zip
	DBPAGE=$$(wget -O - http://www.fda.gov/Drugs/InformationOnDrugs/default.htm --quiet | grep -Eo 'National Drug Code Directory Search(</strong>)*(</a>)*(<br />)*<a href="[a-zA-Z0-9\:/\.]+">More information about the database</a>' | cut -d \" -f 2); \
	LINK=$$(wget -O - http://www.fda.gov/$${DBPAGE} --quiet | grep ">NDC Database File" | cut -d \" -f 2) ; \
	wget -O $@ http://www.fda.gov/$${LINK}
	cd databases/fda_ndc && unzip -e ../fda_ndc.zip

.PHONY: databases/drugbank.xml.zip
databases/drugbank.xml.zip:
	rm -fr databases/drugbank*
	mkdir -p databases/drugbank
	wget -O $@ http://www.drugbank.ca/system/downloads/current/drugbank.xml.zip
	cd databases/drugbank && unzip -e ../drugbank.xml.zip