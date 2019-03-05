TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,display_methods.py
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)

prod: tests
	git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	# this loop works but won't stop the build!
	#for f in $(TEST_FILES); \
	#do \
	#	python3 $$f; \
	#done
	python3 $(TESTDIR)/test_agent.py
	python3 $(TESTDIR)/test_composite.py
	python3 $(TESTDIR)/test_env.py
	python3 $(TESTDIR)/test_itime.py
	python3 $(TESTDIR)/test_space.py

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
