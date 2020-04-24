TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = 
# PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,__main__.py,scheduler.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

# this must be fixed to run pytests!
tests: lint pytests

pytests: FORCE
	nosetests --exe --with-coverage --cover-package=ml

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

# test a python file:
%.py: FORCE
	$(PYLINT) $(PYLINTFLAGS) $@
	nosetests tests.test_$* --nocapture

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
