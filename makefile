# Need to export as ENV var
export TEMPLATE_DIR = templates

# Set up some variables for directories we'll use:
BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)
DOCKER_DIR = docker
REQ_DIR = $(DOCKER_DIR)
REPO = indras_net
MODELS_DIR = models
NB_DIR = notebooks
WEB_DIR = webapp
WEB_PUBLIC = $(WEB_DIR)/public
WEB_BUILD = $(WEB_DIR)/build
WEB_SRC = $(WEB_DIR)/src
WEB_HOMEPAGE = index.html
API_DIR = APIServer
PYLINT = flake8
PYLINTFLAGS = 
PYTHONFILES = $(shell ls $(MODELS_DIR)/*.py)
WEBFILES = $(shell ls $(WEB_SRC)/*.js)
WEBFILES += $(shell ls $(WEB_SRC)/components/*.js)
WEBFILES += $(shell ls $(WEB_SRC)/*.css)

UTILS_DIR = utils
PTML_DIR = html_src
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

FORCE:

notebooks: $(PYTHONFILES)
	cd $(NB_DIR); make notebooks

local: $(HTMLFILES) $(INCS)

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

create_dev_env:
	pip3 install -r $(REQ_DIR)/requirements-dev.txt
	git submodule init $(UTILS_DIR)
	git submodule update $(UTILS_DIR)
	@echo 'Set PYTHONPATH and INDRA_HOME in your login script as follows:'
	@echo 'export INDRA_HOME="$(shell pwd)"'
	@echo 'export PYTHONPATH="$$INDRA_HOME:$$PYTHONPATH"'

setup_react:
	cd $(WEB_DIR); npm install

# Build react files to generate static assets (HTML, CSS, JS)
webapp: $(WEB_PUBLIC)/$(WEB_HOMEPAGE)

$(WEB_PUBLIC)/$(WEB_HOMEPAGE): $(WEBFILES)
	- rm -r static || true
	- cd $(WEB_DIR) && \
	npm run build && \
	cp -r build/* .. && \
	cd ..

deploy_webapp: webapp
	git add static/js/*js
	git add static/js/*map
	git add $(WEB_BUILD)/static/js/*js
	git add $(WEB_BUILD)/static/js/*map
	git add $(WEB_BUILD)/$(WEB_HOMEPAGE)
	cd $(WEB_DIR); npm run deploy

# build tags file for vim:
tags: FORCE
	ctags --recurse .
	git add tags

submods:
	cd utils; git pull origin master

# run tests then commit all, then push
prod: local pytests js notebooks github

# run tests then push just what is already committed:
prod1: tests
	- git pull origin master
	git push origin master

tests: pytests jstests dockertests

python: pytests github

js: jstests deploy_webapp

pytests: FORCE
	cd models; make tests
	cd APIServer; make tests
	cd indra; make tests
	cd ml; make tests
	# cd capital; make tests

jstests: FORCE
	cd webapp; make tests

dockertests:
	docker build -t gcallah/$(REPO) docker/

github:
	- git commit -a
	- git pull origin master
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(DOCKER_DIR)/requirements.txt $(DOCKER_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker

# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(DOCKER_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

# deploy prod containerr
deploy_container: prod_container
	docker push gcallah/$(REPO):latest


nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm models/.coverage

# Build the webapp react docker image
webapp-image:
	docker build -f webapp/Dockerfile.dev -t gcallah/indras_webapp webapp
