import antlr4
from tsynth.grammars.TermLexer import TermLexer
from tsynth.grammars.TermParser import TermParser
from tsynth.parsers import Constraint_Extractor

import z3
import tsynth.util as util

class Text_SyGuS_Spec:
    def __init__(self):
        self.logic = ""
        self.synth_funcs = {}
        self.variables = {}
        self.constraints = []

class SyGuS_Spec:
    def __init__(self, text_spec):
        self.logic = text_spec.logic
        self.variables = text_spec.variables
        self.z3_variables = self._initialise_z3_variables(text_spec.variables)
        self.synth_funcs = self._initialise_synth_funcs(text_spec.synth_funcs)
        self.goal = self._initialise_goal(text_spec)
        
    def _initialise_z3_variables(self, text_vars):
        z3_variables = []
        for var in text_vars:
            z3_variables.append(z3.Const(var, util.str_to_sort(text_vars[var])))
        return z3_variables

    def _initialise_synth_funcs(self, text_synth_funcs):
        synth_funcs = {}
        for synth_func in text_synth_funcs:
            current_func = text_synth_funcs[synth_func]

            inputs = map(util.str_to_sort, current_func['inputs'].values())
            output = util.str_to_sort(current_func['output_sort'])

            synth_func_declaration = z3.Function(synth_func, *inputs, output)
            synth_funcs[synth_func] = {
                'decl' : synth_func_declaration, 
                'inputs' : current_func['inputs'], 
                'output_sort' :  current_func['output_sort'],
                'grammar' : current_func['grammar']
            }

        return synth_funcs

    def _initialise_goal(self, text_spec):
        constraints = []

        for original_constraint in text_spec.constraints:
            constraint_lexer = TermLexer(antlr4.InputStream(original_constraint))
            constraint_stream = antlr4.CommonTokenStream(constraint_lexer)
            constraint_parser = TermParser(constraint_stream)
            constraint_tree = constraint_parser.term()

            constraint_extractor = Constraint_Extractor(text_spec.logic, text_spec.variables, text_spec.synth_funcs)
            constraint = constraint_extractor.visit(constraint_tree)

            constraints.append(constraint)

        goal = z3.BoolVal(True)
        
        for constraint in constraints:
            goal = z3.And(goal, constraint)

        return z3.simplify(goal)

    