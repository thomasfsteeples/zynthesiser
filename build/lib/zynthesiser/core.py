# Parsing Dependencies
import antlr4
from zynthesiser.grammars.SyGuS_v1Lexer import SyGuS_v1Lexer
from zynthesiser.grammars.SyGuS_v1Parser import SyGuS_v1Parser

# Internal Dependencies
from zynthesiser.string_z3_conversion import expr_string_to_z3, z3_to_expr_string
from zynthesiser.SyGuS_Spec import Text_SyGuS_Spec, SyGuS_Spec
from zynthesiser.CFG import CFG, Word_Generator
import zynthesiser.util as util

from zynthesiser.parsers import SyGuS_Extractor

# External Dependencies
import sys
import z3
import time

def parse_sygus_file(sygus_file):
    input_stream = antlr4.FileStream(sygus_file)
    lexer = SyGuS_v1Lexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = SyGuS_v1Parser(stream)
    tree = parser.sygus()

    text_spec = Text_SyGuS_Spec()
    extractor = SyGuS_Extractor(text_spec)
    extractor.visit(tree)

    spec = SyGuS_Spec(text_spec)

    return spec

class Zynthesiser:
    def __init__(self, spec):
        self.spec = spec
        if len(spec.variables) > 0:
            self.universally_quantified = True
        else:
            self.universally_quantified = False
        self.counter_examples = []

    def test_candidate(self, synth_func, candidate_word):
        candidate = expr_string_to_z3(candidate_word, self.spec.logic, synth_func['inputs'])
        substituted_goal = util.substitute_function_for_expression(self.spec.goal, synth_func['decl'], synth_func['z3_inputs'], candidate)

        if self.universally_quantified:

            counter_example_constraints = [z3.BoolVal(True)]

            for counter_example in self.counter_examples:
                counter_example_constraints.append(
                    z3.simplify(z3.substitute(
                        substituted_goal, 
                        list(zip(self.spec.z3_variables, counter_example))))
                )

            counter_example_constraint = z3.simplify(z3.And(*counter_example_constraints))

            if counter_example_constraint.eq(z3.BoolVal(False)):
                return 'sat'
            if ~counter_example_constraint.eq(z3.BoolVal(True)):
                substituted_goal = z3.And(substituted_goal, counter_example_constraint)
            
        else:
            if substituted_goal.eq(z3.BoolVal(True)):
                return 'unsat'
            if substituted_goal.eq(z3.BoolVal(False)):
                return 'sat'

        new_goal = z3.simplify(z3.Not(substituted_goal))

        s = z3.Solver()
        s.add(new_goal)

        validity = str(s.check())
        if validity == 'sat':
            counter_example = []
            model = s.model()
            for var in self.spec.z3_variables:
                counter_example.append(model.eval(var))
            self.counter_examples.append(counter_example)

        return validity

    def solve(self, limit):
        if len(self.spec.synth_funcs) > 1:
            print("zynthesiser does not support synthesis of multiple functions at this time")
            return ''

        synth_func = self.spec.synth_funcs[list(self.spec.synth_funcs.keys())[0]]

        cfg = CFG(synth_func['grammar'])
        function_generator = Word_Generator(cfg, self.spec.logic, synth_func['inputs'])

        counter_examples = []

        for i in range(1, limit+1):
            print("Entered depth {}".format(i))
            start = time.time()

            start_symb = function_generator.cfg.start_symbol
            words = function_generator.generate(start_symb, i)
            elapsed = time.time() - start
            print("Function generation at depth {} took {} seconds".format(i, elapsed))
            print("{} candidates to try".format(len(words)))
            start = time.time()
            for word in words:
                validity = self.test_candidate(synth_func, word)
                if validity == 'unsat':
                    elapsed = time.time() - start
                    print("z3 at depth {} took {} seconds".format(i, elapsed))
                    return word
            elapsed = time.time() - start
            print("z3 at depth {} took {} seconds".format(i, elapsed))
            print()
        print("No suitable function found.")
        return ''