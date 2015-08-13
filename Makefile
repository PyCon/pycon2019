.PHONY: all test flake8 docs

MAKEFLAGS = silent

TEST_COMMAND = $(VIRTUAL_ENV)/bin/django-admin.py

DJANGO_SETTINGS_MODULE = pycon.settings.test

all: flake8 test

test:
	$(TEST_COMMAND) test --noinput --settings=$(DJANGO_SETTINGS_MODULE)

flake8:
	$(info ----Flake8 report----)
	@flake8 pycon
	@flake8 symposion

# If 'make docs' fails, try pip installing requirements/docs.txt
docs:
	(cd docs; DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) make html)
