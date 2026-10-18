book:
	latexmk -pdf -interaction=nonstopmode main.tex
check:
	cd companion && python3 -m vcc.run all && python3 -m unittest discover tests
clean:
	latexmk -C
