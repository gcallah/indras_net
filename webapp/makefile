JSLINT = ./node_modules/.bin/eslint
JSFILES = src

tests: install lint jstests

install:
	npm install

lint:
	$(JSLINT) $(JSFILES)

jstests:
	npm test