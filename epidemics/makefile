TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = # --exclude=old_edgebox.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

tests: pytests lint

pytests: FORCE
	nosetests --exe --with-coverage --cover-package=epidemics

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
