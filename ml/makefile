TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,__main__.py,scheduler.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))


tests: test_used_cars lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

test_used_cars:
	nosetests tests.test_used_cars --nocapture

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
