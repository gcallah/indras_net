JSLINT = ./node_modules/.bin/eslint
JSFILES = src

tests: install lint jstests

install:
	npm install

lint:
	$(JSLINT) $(JSFILES)

jstests:
	./node_modules/.bin/cross-env CI=true npm test -- --coverage --watchAll=false
