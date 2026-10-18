"""Command line: python3 -m vcc.run [all | p03 | p05 | p09 | p10 | p22 | p23]
with toggles --infinite (p03), --coupling (p10), --spread S (p22)."""
import argparse
import sys
from fractions import Fraction

from . import checks


def main(argv=None):
    ap = argparse.ArgumentParser(prog="vcc.run")
    ap.add_argument("which", nargs="?", default="all",
                    choices=["all", "p03", "p05", "p09", "p10", "p22", "p23", "h3", "h4", "book"])
    ap.add_argument("--infinite", action="store_true", help="p03: drop finiteness")
    ap.add_argument("--coupling", action="store_true", help="p10: shared crew")
    ap.add_argument("--spread", type=Fraction, default=None,
                    help="p22: bid-ask spread (a fraction, e.g. 1/10)")
    a = ap.parse_args(argv)
    failed = 0
    if a.which == "all":
        todo = checks.ALL
    else:
        todo = [(a.which.upper(), {
            "p03": lambda: checks.check_p03(infinite=a.infinite),
            "p05": checks.check_p05,
            "p09": checks.check_p09,
            "p10": lambda: checks.check_p10(coupling=a.coupling),
            "p22": lambda: checks.check_p22(a.spread),
            "p23": checks.check_p23,
            "h3": checks.check_h3,
            "h4": checks.check_h4,
            "book": checks.check_book,
        }[a.which])]
    for name, fn in todo:
        ok, detail = fn()
        print("%-45s %s\n    %s" % (name, "PASS" if ok else "FAIL", detail))
        failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
