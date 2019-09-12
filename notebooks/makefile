# Need to export as ENV var
export TEMPLATE_DIR = templates

REPO = indras_net
MODELS_DIR = ../models
MODELFILES = $(shell ls $(MODELS_DIR)/*.py)
NBFILES = $(shell ls $(MODELS_DIR)/*.py | sed -e 's/.py/.ipynb/' | sed 's/\.\.\/models\///')

FORCE:

notebooks: $(NBFILES)

%.ipynb: $(MODELS_DIR)/%.py
	python3 create_model_notebooks.py $< $@
	git add $@
