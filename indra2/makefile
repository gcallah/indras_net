PYLINT = flake8
PYLINTFLAGS = 
PYTHONFILES = $(shell ls *.py)

test:
	python3 ./test_entity.py
	python3 ./test_composite.py

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
