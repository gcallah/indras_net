BOX_DIR = bigbox
BOX_DATA = $(BOX_DIR)/data
BOXPLOTS = $(shell ls $(BOX_DATA)/plot*.pdf)

dist: setup.py
	-git commit -a -m "Building new distribution"
	git push origin master
	python3 setup.py sdist upload	

boxdata:
	./all_box_plots.sh
	-git commit -a -m "Building new Big Box data sets."
	git push origin master
