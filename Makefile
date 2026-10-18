book:
	latexmk -pdf -interaction=nonstopmode main.tex
check:
	cd companion && python3 -m vcc.run all && python3 -m unittest discover tests
	python3 simulator/build.py && node simulator/test_simulator.js
fixture:
	python3 simulator/make_fixture.py
simulator:
	python3 simulator/build.py
clean:
	latexmk -C
