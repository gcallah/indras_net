JSLINT = ./node_modules/.bin/eslint
JSFILES = src

tests: lint install jstests

lint:
	$(JSLINT) $(JSFILES)

install:
	npm install

jstests:
	npm test