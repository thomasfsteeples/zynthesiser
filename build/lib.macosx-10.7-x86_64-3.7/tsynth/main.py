
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

def test_candidate(spec, synth_func, candidate_word):
    candidate = expr_string_to_z3(candidate_word, spec.logic, synth_func['inputs'], [])
    s = z3.Solver()

    substituted_goal = util.substitute_function_for_expression(spec.goal, synth_func['decl'], synth_func['z3_inputs'], candidate)
    new_goal = z3.simplify(z3.Not(z3.ForAll(spec.z3_variables, substituted_goal)))

    s.add(new_goal)
    validity = str(s.check())
    return validity

def solve(spec, limit):
    synth_func = spec.synth_funcs[list(spec.synth_funcs.keys())[0]]

    cfg = CFG(synth_func['grammar'])
    function_generator = Word_Generator(cfg, spec.logic, synth_func['inputs'], [])

    for i in range(1, limit):
        print("Entered depth {}".format(i))
        start = time.time()
        words = function_generator.generate('S0', i)
        elapsed = time.time() - start
        print("Function generation at depth {} took {} seconds".format(i, elapsed))
        print("{} candidates to try".format(len(words)))
        print()
        for word in words:
            validity = test_candidate(spec, synth_func, word)
            if validity == 'unsat':
                return word
    return ''

def main():
    spec = parse_sygus_file(sys.argv[1])

    if len(spec.synth_funcs) > 1:
        print("zynthesiser does not support synthesis of multiple functions at this time")
        sys.exit()

    limit = 11

    candidate = solve(spec, limit)

    print(candidate)            

if __name__ == '__main__':
    main()