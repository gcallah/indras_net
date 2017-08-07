
dist: setup.py
	git commit -a -m "Building new distribution"
	git push origin master
	python setup.py sdist upload	
