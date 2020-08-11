TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --exclude=__main__.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: FORCE
	./pytests.sh capture

tests: pytests lint

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
