PYLINT = flake8
PYLINTFLAGS = --exclude=interactive.py,__main__.py
PYTHONFILES = $(shell ls *.py)

FORCE:

tests: pytests lint

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh

tests: pytests lint

# test a python file:
%.py: FORCE
	$(PYLINT) $(PYLINTFLAGS) $@
	nosetests tests.test_$* --nocapture

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

