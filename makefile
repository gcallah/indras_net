BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)
DOCKER_DIR = docker
REPO = indras_net
MODELS_DIR = models
API_DIR = APIServer
PYLINT = flake8
PYLINTFLAGS = 
PYTHONFILES = $(shell ls $(API_DIR)/*.py)
PYTHONFILES += $(shell ls $(MODELS_DIR)/*.py)

FORCE:

tags: FORCE
	ctags --recurse .

# run tests then commit
prod: tests
	- git commit -a
	git push origin master
	ssh indrasnet@ssh.pythonanywhere.com 'cd /home/indrasnet/indras_net; /home/indrasnet/indras_net/rebuild.sh'

tests: FORCE
	cd indra; make tests
	cd models; make tests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile $(DOCKER_DIR)/requirements.txt $(DOCKER_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker
	docker push gcallah/$(REPO)-dev:latest

# prod container has only what's needed to run
prod_container: $(DOCKER_DIR)/Deployable $(DOCKER_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/$(REPO) docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

deploy_container:
	docker push gcallah/$(REPO):latest

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv

# Build react files to generate static assets (HTML, CSS, JS)
build-webapp:
	- rm -r static || true
	- rm webapp.html || true
	- cd webapp && \
	npm run build && \
	mv build/index.html build/webapp.html && \
	cp -r build/* .. && \
	cd ..

# Build the webapp react docker image
webapp-image:
	docker build -f webapp/Dockerfile.dev -t gcallah/indras_webapp webapp

# Mount resources and run the react webapp
webapp-run:
	docker run --rm -p 3000:3000 -v `pwd`/webapp/public:/home/public -v `pwd`/webapp/src:/home/src --name webapp-dev-container gcallah/indras_webapp

# Mount resources and explore the react webapp image
webapp-run-interactive:
	docker run --rm -it -p 3000:3000 -v `pwd`/webapp/public:/home/public -v `pwd`/webapp/src:/home/src --name webapp-dev-container gcallah/indras_webapp sh
