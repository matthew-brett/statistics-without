presentation=index.qmd

slides: $(presentation)
	quarto render $(presentation) --to revealjs --output-dir _build
