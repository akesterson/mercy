MAJOR:=$(shell bash -c 'source version.sh ; echo $$MAJOR')
BUILD:=$(shell bash -c 'source version.sh ; echo $$BUILD')
MODULEPATH:=$(shell puppet config print modulepath)
ifeq ($(MODULEPATH),)
$(error "I can't figure out your puppet modulepath, this will cause all kinds of bad things to happen with 'make install' and 'make uninstall'")
endif
PUPPET_DEPS=$(find mercy -type f)
PUPPET_DIST=mercy/pkg/akesterson-mercy-$(MAJOR).$(BUILD).tar.gz

.PHONY: clean
clean:
	rm pkg/*
	rm Modulefile

mercy/Modulefile: Modulefile.template.sh version.sh
	source version.sh && bash Modulefile.template.sh > Modulefile

$(PUPPET_DIST): $(PUPPET_DEPS) mercy/Modulefile
	rm -f $(PUPPET_DIST)
	mkdir -p $$(dirname $(PUPPET_DIST))
	echo 'We would use puppet module tool here but we dont because it doesnt work on windows buildhosts and cant upload from the command line anyway'
	tar --exclude=mercy/Modulefile --exclude=mercy/pkg -czvf $(PUPPET_DIST) mercy/

dist: $(PUPPET_DIST)

all: $(PUPPET_DIST)

install: $(PUPPET_DIST)
	tar -zxvf $(PUPPET_DIST) -C $(MODULEPATH)

uninstall:
	rm -fr $(MODULEPATH)/mercy