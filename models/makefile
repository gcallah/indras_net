TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --exclude=interactive.py,__main__.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	./pytests.sh capture

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

test_models:
	nosetests tests.test_models

test_bacteria:
	$(PYLINT) $(PYLINTFLAGS) coop.py
	nosetests tests.test_bacteria --nocapture

test_coop:
	$(PYLINT) $(PYLINTFLAGS) coop.py
	nosetests tests.test_coop --nocapture

test_el_farol:
	$(PYLINT) $(PYLINTFLAGS) el_farol.py
	nosetests tests.test_el_farol --nocapture

test_ex:
	$(PYLINT) $(PYLINTFLAGS) ex_boyfriend.py
	nosetests tests.test_ex_boyfriend --nocapture

test_fmarket:
	$(PYLINT) $(PYLINTFLAGS) fmarket.py
	nosetests tests.test_fmarket --nocapture

test_forestfire:
	$(PYLINT) $(PYLINTFLAGS) forestfire.py
	nosetests tests.test_forestfire --nocapture

test_segregation:
	$(PYLINT) $(PYLINTFLAGS) segregation.py
	nosetests tests.test_segregation --nocapture

test_wolfsheep:
	$(PYLINT) $(PYLINTFLAGS) wolfsheep.py
	nosetests tests.test_wolfsheep --nocapture

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
