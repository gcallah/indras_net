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

test_bigbox:
	nosetests tests.test_bigboxV2 --nocapture

test_coop:
	$(PYLINT) $(PYLINTFLAGS) coop.py
	nosetests tests.test_coop --nocapture

test_drunks:
	$(PYLINT) $(PYLINTFLAGS) drunks.py
	nosetests tests.test_drunks --nocapture

test_ex:
	$(PYLINT) $(PYLINTFLAGS) ex_boyfriend.py
	nosetests tests.test_ex_boyfriend --nocapture

test_forestfire:
	$(PYLINT) $(PYLINTFLAGS) forestfire.py
	nosetests tests.test_forestfire --nocapture

test_gameoflife:
	$(PYLINT) $(PYLINTFLAGS) gameoflife.py
	nosetests tests.test_gameoflife --nocapture

test_seg:
	nosetests tests.test_segregation --nocapture

test_sand:
	nosetests tests.test_sandpile --nocapture

test_sched:
	nosetests tests.test_scheduler --nocapture

# for some reason the following test hangs:
test_fashion:
	nosetests tests.test_fashion

test_segregation:
	nosetests tests.test_segregation

test_wolfram:
	nosetests tests.test_wolfram --nocapture

test_wolfsheep:
	nosetests tests.test_wolfsheep --nocapture

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
