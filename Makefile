.PHONY: all test flake8

MAKEFLAGS = silent

TEST_COMMAND = $(VIRTUAL_ENV)/bin/django-admin.py

DJANGO_SETTINGS_MODULE = pycon.settings.test

all:
	make test
	make flake8

test:
	$(TEST_COMMAND) test --noinput --settings=$(DJANGO_SETTINGS_MODULE)

flake8:
	$(info ----Flake8 report----)
	@flake8 pycon
	@flake8 symposion
