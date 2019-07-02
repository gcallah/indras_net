TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,__main__.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	./pytests.sh

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

test_seg:
	nosetests tests.test_segregation --nocapture

test_sand:
	nosetests tests.test_sandpile --nocapture

test_sched:
	nosetests tests.test_scheduler --nocapture

# for some reason the following test hangs:
# test_fashion:
# 	nosetests tests.test_fashion

test_wolfram:
	nosetests tests.test_wolfram --nocapture

test_wolfsheep:
	nosetests tests.test_wolfsheep --nocapture

test_forestfire:
	nosetests tests.test_forestfire --nocapture

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
