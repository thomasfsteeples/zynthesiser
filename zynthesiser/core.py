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
        self._macros_decls = []
        for macro in self.spec.macros:
            self._macros_decls.append(self.spec.macros[macro]['decl'])

    def test_candidate(self, synth_func, candidate):
        # candidate = expr_string_to_z3(candidate_word, self.spec, synth_func['inputs'])

        goal = util.substitute_function_for_expression(
            self.spec.goal, 
            synth_func['decl'], 
            synth_func['z3_inputs'], 
            candidate
        )
        
        while(True):
            macro_decl = util.contains_funcs(goal, self._macros_decls)
            if macro_decl is None:
                break
            macro_name = macro_decl.name()
            macro = self.spec.macros[macro_name]
            macro_def = expr_string_to_z3(macro['definition'], self.spec, macro['inputs'])
            macro_params = macro['z3_inputs']
            goal = util.substitute_function_for_expression(
                goal,
                macro_decl,
                macro_params,
                macro_def
            )

        if self.universally_quantified:

            counter_example_constraints = [z3.BoolVal(True)]

            for counter_example in self.counter_examples:
                counter_example_constraints.append(
                    z3.simplify(z3.substitute(
                        goal, 
                        list(zip(self.spec.z3_variables, counter_example))))
                )

            counter_example_constraint = z3.simplify(z3.And(*counter_example_constraints))

            if counter_example_constraint.eq(z3.BoolVal(False)):
                return 'sat'
            if ~counter_example_constraint.eq(z3.BoolVal(True)):
                goal = z3.And(goal, counter_example_constraint)
            
        else:
            if goal.eq(z3.BoolVal(True)):
                return 'unsat'
            if goal.eq(z3.BoolVal(False)):
                return 'sat'

        goal = z3.simplify(z3.Not(goal))

        s = z3.Solver()
        s.add(goal)

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
        function_generator = Word_Generator(cfg, self.spec, synth_func)

        for i in range(1, limit+1):
            # print("Entered depth {}".format(i))
            # start = time.time()

            start_symb = function_generator.cfg.start_symbol
            words = function_generator.generate(start_symb, i)
            # elapsed = time.time() - start
            # print("Function generation at depth {} took {} seconds".format(i, elapsed))
            # print("{} candidates generated".format(len(words)))
            start_symb = function_generator.cfg.start_symbol
            # start = time.time()
            pruned_candidates = set()
            for word in words:
                z3_expr = z3.simplify(expr_string_to_z3(word, self.spec, synth_func['inputs']))
                pruned_candidates.add(z3_expr)
            # elapsed = time.time() - start
            # print("Conversion and pruning took {} seconds".format(elapsed))
            # print("{} candidates remain".format(len(pruned_candidates)))
            # start = time.time()
            for candidate in pruned_candidates:
                validity = self.test_candidate(synth_func, candidate)
                if validity == 'unsat':
                    elapsed = time.time() - start
                    print("z3 at depth {} took {} seconds".format(i, elapsed))
                    return candidate
            # elapsed = time.time() - start
            # print("z3 at depth {} took {} seconds".format(i, elapsed))
            # print()
        print("No suitable function found.")
        return ''