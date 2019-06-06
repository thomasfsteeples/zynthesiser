import z3
import zynthesiser as zn
import sys

spec = zn.parse_sygus_file(sys.argv[1])

zyn = zn.Zynthesiser(spec)
print(zyn.solve(15))