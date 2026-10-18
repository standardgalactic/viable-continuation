import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fractions import Fraction
from vcc import checks


class TestProgramme(unittest.TestCase):
    def test_all_named_checks(self):
        for name, fn in checks.ALL:
            ok, detail = fn()
            self.assertTrue(ok, "%s: %s" % (name, detail))

    def test_spread_threshold(self):
        # arbitrage disappears once the spread exceeds 1/6
        self.assertIn("negative cycle", checks.check_p22(Fraction(1, 10))[1])
        self.assertIn("potential exists", checks.check_p22(Fraction(1, 5))[1])


if __name__ == "__main__":
    unittest.main()
