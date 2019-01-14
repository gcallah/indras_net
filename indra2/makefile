TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py
PYTHONFILES = $(shell ls *.py)

prod: test
	git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytest: $(PYTHONFILES)
	python3 $(TESTDIR)/test_entity.py
	python3 $(TESTDIR)/test_composite.py

test: lint pytest

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
