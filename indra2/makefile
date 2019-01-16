TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py
PYTHONFILES = $(shell ls *.py)

prod: tests
	git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	python3 $(TESTDIR)/test_entity.py
	python3 $(TESTDIR)/test_composite.py
	python3 $(TESTDIR)/test_itime.py

tests: lint pytests

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
