BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)
DOCKER_DIR = docker
DJANGO_DIR = IndrasNet
REPO = indras_net
MODELS_DIR = models
PYLINT = flake8
PYLINTFLAGS = 
PYTHONFILES = $(shell ls $(DJANGO_DIR)/*.py)
PYTHONFILES += $(shell ls $(MODELS_DIR)/*.py)

tags:
	ctags --recurse .

prod: $(SRCS) $(OBJ)
	cd indra; make prod

# this now cutover to new indra:
pytests:
	cd indra; make pytests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

db: $(DJANGO_DIR)/models.py
	python ./manage.py makemigrations IndrasNet
	python ./manage.py migrate
	git add IndrasNet/migrations/*.py
	git add $(DJANGO_DIR)/migrations/*.py
	-git commit $(DJANGO_DIR)/migrations/*.py
	git push origin master

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
