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

prod: $(SRCS) $(OBJ)
	./test_functionality.sh
	-git commit -a -m "Building production."
	git push origin master
	ssh indrasnet@ssh.pythonanywhere.com 'cd /home/indrasnet/indras_net; /home/indrasnet/indras_net/rebuild.sh'
