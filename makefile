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

dist: setup.py
	-git commit -a -m "Building new distribution"
	git push origin master
	python3 setup.py sdist upload	

boxdata:
	./all_box_plots.sh
	-git commit -a -m "Building new Big Box data sets."
	git push origin master

prod: $(SRCS) $(OBJ)
	./test/all_tests.sh
	-git commit -a -m "Building production."
	git pull origin master
	git push origin master
	ssh indrasnet@ssh.pythonanywhere.com 'cd /home/indrasnet/indras_net; /home/indrasnet/indras_net/rebuild.sh'

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

dev_container: $(DOCKER_DIR)/Dockerfile $(DOCKER_DIR)/requirements.txt $(DOCKER_DIR)/requirements-dev.txt
	docker build -t gcallah/indra-dev docker
	docker push gcallah/indra-dev:latest

prod_container: $(DOCKER_DIR)/Dockerfile $(DOCKER_DIR)/requirements.txt
	docker system prune -f
	docker build -t gcallah/indra docker --no-cache --build-arg repo=$(REPO) -f $(DOCKER_DIR)/Deployable

deploy_container:
	docker push gcallah/indra:latest

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
