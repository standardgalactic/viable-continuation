"""Loads the shared Housing v2 specification (spec/housing_v2.json).

The chapters, the companion, and the browser simulator all take their
parameters from this one file. Changing a parameter there changes every
description at once, and tests/test_vcc.py fails if the simulator's embedded
copy differs."""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.normpath(os.path.join(_HERE, "..", "..", "spec", "housing_v2.json"))

with open(PATH) as f:
    SPEC = json.load(f)

CORE = SPEC["core"]

# The code uses one maintenance step and one price per tenth, both 100.
assert CORE["maintenance_step"] == 100 and CORE["money_per_tenth"] == 100
