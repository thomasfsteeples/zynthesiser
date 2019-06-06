import antlr4
from zynthesiser.grammars.TermLexer import TermLexer
from zynthesiser.grammars.TermParser import TermParser
from zynthesiser.parsers import Constraint_Extractor

import z3
import zynthesiser.util as util
from zynthesiser.string_z3_conversion import expr_string_to_z3
import re

class Text_SyGuS_Spec:
    def __init__(self):
        self.logic = ""
        self.variables = {}

        self.synth_funcs = {}
        self.uninterpreted_funcs = {}
        self.macros = {}
        
        self.constraints = []

class SyGuS_Spec:
    def __init__(self, text_spec):
        self.logic = text_spec.logic

        self.variables = text_spec.variables
        self.z3_variables = self._initialise_z3_variables(text_spec.variables)

        self.synth_funcs = self._initialise_synth_funcs(text_spec.synth_funcs)
        self.uninterpreted_funcs = self._initialise_uninterpreted_funcs(text_spec.uninterpreted_funcs)
        self.macros = self._initialise_macros(text_spec.macros)

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

            input_sorts = list(map(util.str_to_sort, current_func['inputs'].values()))
            output_sort = util.str_to_sort(current_func['output_sort'])

            inputs = []
            for i, text_input in enumerate(current_func['inputs']):
                inputs.append(z3.Const(text_input, input_sorts[i]))

            synth_func_declaration = z3.Function(synth_func, *input_sorts, output_sort)
            synth_funcs[synth_func] = {
                'decl' : synth_func_declaration, 
                'inputs' : current_func['inputs'],
                'z3_inputs' : inputs,
                'output_sort' :  current_func['output_sort'],
                'z3_output_sort' : output_sort,
                'grammar' : current_func['grammar']
            }

        return synth_funcs

    def _initialise_uninterpreted_funcs(self, text_u_funcs):
        u_funcs = {}
        for u_func in text_u_funcs:
            current_func = text_u_funcs[u_func]

            sorts = list(map(util.str_to_sort, current_func['sorts']))

            u_funcs[u_func] = {
                'decl' : z3.Function(u_func, *sorts)
            } 
        
        return u_funcs

    def _initialise_macros(self, text_macros):
        macros = {}
        for macro in text_macros:
            current_macro = text_macros[macro]

            input_sorts = list(map(util.str_to_sort, current_macro['inputs'].values()))
            output_sort = util.str_to_sort(current_macro['output_sort'])

            inputs = []
            for i, text_input in enumerate(current_macro['inputs']):
                inputs.append(z3.Const(text_input, input_sorts[i]))

            macro_declaration = z3.Function(macro, *input_sorts, output_sort)
            macro_definition = current_macro['definition'].replace('(', "").replace(')', "")
            macro_definition = ' '.join(macro_definition.split())

            macros[macro] = {
                'decl'              : macro_declaration, 
                'inputs'            : current_macro['inputs'],
                'z3_inputs'         : inputs,
                'output_sort'       : current_macro['output_sort'],
                'z3_output_sort'    : output_sort,
                'definition'        : macro_definition
            }

        return macros

    def _initialise_goal(self, text_spec):
        constraints = []
        funcs = {
            **self.synth_funcs,
            **self.uninterpreted_funcs,
            **self.macros
        }

        for original_constraint in text_spec.constraints:
            constraint_lexer = TermLexer(antlr4.InputStream(original_constraint))
            constraint_stream = antlr4.CommonTokenStream(constraint_lexer)
            constraint_parser = TermParser(constraint_stream)
            constraint_tree = constraint_parser.term()

            constraint_extractor = Constraint_Extractor(self.logic, self.variables, funcs)
            constraint = constraint_extractor.visit(constraint_tree)

            constraints.append(constraint)

        goal = z3.BoolVal(True)
        
        for constraint in constraints:
            goal = z3.And(goal, constraint)

        goal = z3.simplify(goal)

        return z3.simplify(goal)

    