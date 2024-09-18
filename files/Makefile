PRESENTATION=index.qmd
OUTPUT_DIR=_build
OUTPUT_NB=$(patsubst %.qmd,%.ipynb,$(PRESENTATION))
PYTHON ?= python
PIP_INSTALL_CMD ?= $(PYTHON) -m pip install

slides: $(PRESENTATION)
	quarto render $(PRESENTATION) --to revealjs --output-dir $(OUTPUT_DIR)

slides-jl: slides
	# Jupyter-lite files for presentation build.
	$(PIP_INSTALL_CMD) -r py-jl-requirements.txt
	jupytext --to ipynb $(PRESENTATION) -o $(OUTPUT_NB)
	$(PYTHON) -m jupyter lite build \
		--contents . \
		--output-dir $(OUTPUT_DIR)

clean:
	git clean -fxd
