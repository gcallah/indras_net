PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,__main__.py
PYTHONFILES = $(shell ls *.py)

tests: pytests lint

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	./pytests.sh

tests: pytests lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

