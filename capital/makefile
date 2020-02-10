TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --exclude=old_edgebox.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

tests: pytests lint

pytests: $(PYTHONFILES)
	nosetests --exe --with-coverage --cover-package=capital

# you can clone the next two lines and get a test for any module:
test_trade_utils:
	nosetests tests.test_trade_utils

test_cap_struct:
	nosetests tests.test_cap_struct

test_edgeworthbox:
	nosetests tests.test_edgeworthbox

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
