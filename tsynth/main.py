# Parsing Dependencies
import antlr4
from tsynth.grammars.SyGuS_v1Lexer import SyGuS_v1Lexer
from tsynth.grammars.SyGuS_v1Parser import SyGuS_v1Parser

# Internal Dependencies
from tsynth.string_z3_conversion import expr_string_to_z3, z3_to_expr_string
from tsynth.SyGuS_Spec import Text_SyGuS_Spec, SyGuS_Spec
from tsynth.CFG import CFG, Word_Generator
import tsynth.util as util

from tsynth.parsers import SyGuS_Extractor

# External Dependencies
import sys
import z3

def main():
    # Parse SyGuS file and return a partial specification
    input_stream = antlr4.FileStream(sys.argv[1])
    lexer = SyGuS_v1Lexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = SyGuS_v1Parser(stream)
    tree = parser.sygus()

    text_spec = Text_SyGuS_Spec()
    extractor = SyGuS_Extractor(text_spec)
    extractor.visit(tree)

    spec = SyGuS_Spec(text_spec)

    if len(spec.synth_funcs) > 1:
        print("tsynth does not support synthesis of multiple functions at this time")
        sys.exit()

    limit = 7

    candidate = solve(spec, limit)

    print(candidate)

def test_candidate(spec, synth_func_declaration, candidate_word):
    candidate = expr_string_to_z3(candidate_word, spec.logic, spec.variables, [])
    s = z3.Solver()

    substituted_goal = util.substitute_function_for_expression(spec.goal, synth_func_declaration, spec.z3_variables, candidate)
    new_goal = z3.simplify(z3.Not(z3.ForAll(spec.z3_variables, substituted_goal)))

    s.add(new_goal)
    validity = str(s.check())
    return validity

def solve(spec, limit):
    synth_func = spec.synth_funcs[list(spec.synth_funcs.keys())[0]]
    synth_func_declaration = synth_func['decl']

    cfg = CFG(synth_func['grammar'])
    function_generator = Word_Generator(cfg, spec.logic, spec.variables, [])

    for i in range(1, limit):
        words = function_generator.generate('S0', i)
        for word in words:
            validity = test_candidate(spec, synth_func_declaration, word)
            if validity == 'unsat':
                return word
    return ''
            

if __name__ == '__main__':
    main()