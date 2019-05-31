import z3
import zynthesiser as zn

spec = zn.parse_sygus_file('./sl_examples/sl_example_1.sl')

zyn = zn.Zynthesiser(spec)
print(zyn.solve(11))