TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --exclude=good_structure.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

tests: lint  # pytests

pytests: FORCE
	nosetests --exe --with-coverage --cover-package=capital

# test a python file:
%.py: FORCE
	$(PYLINT) $(PYLINTFLAGS) $@
	nosetests tests.test_$* --nocapture

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
