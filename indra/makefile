TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,region.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
SHELL := /bin/bash

export user_type = test

FORCE:

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

# test a python file:
%.py: FORCE
	nosetests tests.test_$* --nocapture
	$(PYLINT) $(PYLINTFLAGS) $@

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
