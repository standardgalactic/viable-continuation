"""Build simulator/housing_v2_simulator.html from template.html and spec/housing_v2.json.

The output is a single self-contained file: the specification is embedded verbatim,
so the page works offline. Run from anywhere: python3 simulator/build.py
"""
import json, pathlib
here = pathlib.Path(__file__).resolve().parent
spec = (here.parent / "spec" / "housing_v2.json").read_text()
json.loads(spec)  # must parse
tpl = (here / "template.html").read_text()
out = tpl.replace("/*SPEC_JSON*/", spec.replace("</", "<\\/"))
(here / "housing_v2_simulator.html").write_text(out)
print("wrote", here / "housing_v2_simulator.html", len(out), "bytes")
