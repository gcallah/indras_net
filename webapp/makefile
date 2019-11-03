JSLINT = ./node_modules/.bin/eslint
JSFILES = $(shell ls -R *.js)

tests: jstests lint

lint: $(patsubst %.js,%.jslint,$(JSFILES))

jstests: $(JSFILES)
	npm build
	npm test

%.jslint:
	$(JSLINT) $*.js