# Need to export as ENV var
export TEMPLATE_DIR = templates

REPO = indras_net
MODELS_DIR = ../models
PYTHONFILES = $(shell ls $(MODELS_DIR)/*.py)

MODELFILES = $(shell ls $(MODELS_DIR)/*.py)

FORCE:

notebooks: $(MODELFILES)

%.ipynb: $(MODELS_DIR)/%.py
	python3 create_model_notebooks.py $<
	git add $@
