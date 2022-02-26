import time
import z3

from itertools import count
from .util import (contains_funcs, substitute_function_for_expression)
from .cfg import CFG
from .sygus_spec import SygusSpec
from .error import ZynthesiserException, get_zynthesiser_logger


def z3_expr_from_sexpr(sexpr: str):
    return z3.BoolVal(True)


class Zynthesiser:

    def __init__(self, spec: SygusSpec):
        self.spec = spec
        if len(spec.variables) > 0:
            self.universally_quantified = True
        else:
            self.universally_quantified = False
        self.counter_examples = []
        self._macros_decls = []
        for macro in self.spec.macros:
            self._macros_decls.append(self.spec.macros[macro]["decl"])

    def test_candidate(self, synth_func, candidate):
        # candidate = expr_string_to_z3(candidate_word, self.spec, synth_func['inputs'])

        goal = substitute_function_for_expression(self.spec.goal,
                                                  synth_func["decl"],
                                                  synth_func["z3_inputs"],
                                                  candidate)

        while True:
            macro_decl = contains_funcs(goal, self._macros_decls)
            if macro_decl is None:
                break
            macro_name = macro_decl.name()
            macro = self.spec.macros[macro_name]
            macro_def = expr_string_to_z3(macro["definition"], self.spec,
                                          macro["inputs"])
            macro_params = macro["z3_inputs"]
            goal = substitute_function_for_expression(goal, macro_decl,
                                                      macro_params, macro_def)

        if self.universally_quantified:
            counter_example_constraints = [z3.BoolVal(True)]
            for counter_example in self.counter_examples:
                counter_example_constraints.append(
                    z3.simplify(
                        z3.substitute(
                            goal,
                            list(zip(self.spec.z3_variables,
                                     counter_example)))))
            counter_example_constraint = z3.simplify(
                z3.And(*counter_example_constraints))
            if counter_example_constraint.eq(z3.BoolVal(False)):
                return "sat"
            if not counter_example_constraint.eq(z3.BoolVal(True)):
                goal = z3.And(goal, counter_example_constraint)
        else:
            if goal.eq(z3.BoolVal(True)):
                return "unsat"
            if goal.eq(z3.BoolVal(False)):
                return "sat"

        goal = z3.simplify(z3.Not(goal))

        s = z3.Solver()
        s.add(goal)

        validity = str(s.check())
        if validity == "sat":
            counter_example = []
            model = s.model()
            for var in self.spec.z3_variables:
                counter_example.append(model.eval(var))
            self.counter_examples.append(counter_example)

        return validity

    def solve(self):
        if len(self.spec.synth_funcs) > 1:
            raise ZynthesiserException(
                "zynthesiser.Zynthesiser.solve: zynthesiser does not support synthesis of multiple functions at this time"
            )

        synth_func = self.spec.synth_funcs[list(
            self.spec.synth_funcs.keys())[0]]

        cfg = CFG(synth_func["grammar"])

        logger = get_zynthesiser_logger()

        for i in count(1):
            logger.info(
                "zynthesiser.Zynthesiser.solve: Entered search depth {}", i)
            start = time.time()

            start_symb = cfg.start_symbol
            words = cfg.generate_words(start_symb, i)
            elapsed = time.time() - start
            logger.info(
                "zynthesiser.Zynthesiser.solve: Function generation at depth {} took {} seconds",
                i, elapsed)
            logger.info(
                "zynthesiser.Zynthesiser.solve: {} candidates generated",
                len(words))

            start = time.time()
            pruned_candidates = set()
            for word in words:
                z3_expr = z3.simplify(
                    expr_string_to_z3(word, self.spec, synth_func["inputs"]))
                pruned_candidates.add(z3_expr)
            elapsed = time.time() - start
            logger.info(
                "zynthesiser.Zynthesiser.solve: Conversion and pruning took {} seconds",
                elapsed)
            logger.info("zynthesiser.Zynthesiser.solve: {} candidates remain",
                         len(pruned_candidates))

            start = time.time()
            for candidate in pruned_candidates:
                validity = self.test_candidate(synth_func, candidate)
                if validity == "unsat":
                    elapsed = time.time() - start
                    logger.info(
                        "zynthesiser.Zynthesiser.solve: z3 at depth {} took {} seconds",
                        i, elapsed)
                    logger.info(
                        "zynthesiser.Zynthesiser.solve: Made {} calls to z3 in total",
                        len(self.counter_examples))
                    return candidate
            elapsed = time.time() - start
            logger.info(
                "zynthesiser.Zynthesiser.solve: z3 at depth {} took {} seconds",
                i, elapsed)
        print("zynthesiser.Zynthesiser.solve: No suitable function found.")
