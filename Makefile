PRESENTATION=index.qmd
OUTPUT_DIR=_build
NB_DIR=_notebooks
OUTPUT_NB=$(NB_DIR)/$(patsubst %.qmd,%.ipynb,$(PRESENTATION))
PYTHON ?= python
PIP_INSTALL_CMD ?= $(PYTHON) -m pip install

slides: $(PRESENTATION)
	quarto render $(PRESENTATION) --to revealjs --output-dir $(OUTPUT_DIR)

slides-jl: slides
	# Jupyter-lite files for presentation build.
	$(PIP_INSTALL_CMD) -r py-jl-requirements.txt
	mkdir -p $(NB_DIR)
	jupytext --to ipynb $(PRESENTATION) -o $(OUTPUT_NB)
	cp -r images $(NB_DIR)
	sed -i '' 's/"name": "python.*"/"name": "python"/g' $(OUTPUT_NB)
	$(PYTHON) -m jupyter lite build \
		--contents $(NB_DIR) \
		--output-dir $(OUTPUT_DIR)/interact

clean:
	git clean -fxd
