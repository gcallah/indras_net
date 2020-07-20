JSLINT = ./node_modules/.bin/eslint --fix
JSFILES = src

tests: lint jstests

install:
	npm install

lint:
	$(JSLINT) $(JSFILES)

jstests:
	./node_modules/.bin/cross-env CI=true npm test -- --coverage --watchAll=false
