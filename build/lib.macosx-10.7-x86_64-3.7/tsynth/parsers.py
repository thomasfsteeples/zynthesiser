import antlr4
from tsynth.grammars.SyGuS_v1Lexer import SyGuS_v1Lexer
from tsynth.grammars.SyGuS_v1Parser import SyGuS_v1Parser
from tsynth.grammars.SyGuS_v1Visitor import SyGuS_v1Visitor

from tsynth.grammars.TermLexer import TermLexer
from tsynth.grammars.TermParser import TermParser
from tsynth.grammars.TermVisitor import TermVisitor

import tsynth.util as util
from tsynth.Symbol_Mapper import Symbol_Mapper

import z3

class SyGuS_Extractor(SyGuS_v1Visitor):
    def __init__(self, spec):
        super().__init__()
        self.spec = spec

    def visitSet_logic_cmd(self, ctx:SyGuS_v1Parser.Set_logic_cmdContext):
        self.spec.logic = ctx.SYMBOL().getText()

    def visitSynth_fun_cmd(self, ctx:SyGuS_v1Parser.Synth_fun_cmdContext):
        # Create object that describes the given synthesis function
        synth_func = {}

        symbols = ctx.SYMBOL()
        sorts = ctx.sort_expr()
        # Extract the given name
        synth_func_name = symbols[0].getText()
        synth_func['inputs'] = {}

        for sym, sort in zip(symbols[1:], sorts[:-1]):
            synth_func['inputs'][sym.getText()] = sort.getText()

        synth_func['output_sort'] = sorts[-1].getText()

        synth_func['grammar'] = {}

        non_terminals = ctx.nt_def()
        for nt in non_terminals:
            nt_grammar = self.visit(nt)
            synth_func['grammar'].update(nt_grammar)

        # Put function into spec
        self.spec.synth_funcs[synth_func_name] = synth_func

    def visitNt_def(self, ctx:SyGuS_v1Parser.Nt_defContext):
        nt = ctx.SYMBOL().getText()
        g_terms = ctx.g_term()
        rules = []

        for g_term in g_terms: 
            rule_text = g_term.start.getInputStream().getText(g_term.start.start, g_term.stop.stop)

            rule_lexer = TermLexer(antlr4.InputStream(rule_text))
            rule_stream = antlr4.CommonTokenStream(rule_lexer)
            rule_parser = TermParser(rule_stream)
            rule_tree = rule_parser.g_term()

            rule_extractor = Rule_Extractor()
            rule = rule_extractor.visit(rule_tree)

            rules.append(rule)

        return {nt : rules}


    def visitVar_decl_cmd(self, ctx:SyGuS_v1Parser.Var_decl_cmdContext):
        self.spec.variables[ctx.SYMBOL().getText()] = ctx.sort_expr().getText()
    
    def visitConstraint_cmd(self, ctx:SyGuS_v1Parser.Constraint_cmdContext):
        constraint = ctx.term()
        original_constraint = constraint.start.getInputStream().getText(constraint.start.start, constraint.stop.stop)
        
        self.spec.constraints.append(original_constraint)



class Constraint_Extractor(TermVisitor):
    def __init__(self, logic, variables, funcs):
        super().__init__()
        self.logic = logic
        self.variables = variables
        self.funcs = funcs

    def visitFunc_term(self, ctx:TermParser.Func_termContext):
        symbol = ctx.SYMBOL().getText()
        if symbol in self.funcs:
            current_func =  self.funcs[symbol]

            inputs = map(util.str_to_sort, current_func['inputs'].values())
            output = util.str_to_sort(current_func['output_sort'])

            f = z3.Function(symbol, *inputs, output)
        else:
            f = Symbol_Mapper.get_function_from_symbol(symbol, self.logic)

        children = []
        for term in ctx.term():
            children.append(self.visit(term))
        return f(*children)

    def visitP_int_literal(self, ctx:TermParser.P_int_literalContext):
        return z3.IntVal(ctx.POSITIVE_INT_CONST().getText())

    def visitN_int_literal(self, ctx:TermParser.N_int_literalContext):
        return z3.IntVal(ctx.NEGATIVE_INT_CONST().getText())

    def visitReal_literal(self, ctx:TermParser.Real_literalContext):
        return z3.RealVal(ctx.REAL_CONST().getText())

    def visitBool_literal(self, ctx:TermParser.Bool_literalContext):
        return z3.BoolVal(ctx.BOOL_CONST().getText())

    def visitBv_literal(self, ctx:TermParser.Bv_literalContext):
        bv_lit = ctx.BV_CONST().getText()
        lit = 0
        if bv_lit[:2] == '0x':
            lit = int(bv_lit, 16)
            width = (len(bv_lit) - 2) * 4
        else:
            lit = int(bv_lit, 2)
            width = len(bv_lit) - 2
        return z3.BitVecVal(lit, width)

    def visitSymbol_term(self, ctx:TermParser.Symbol_termContext):
        symbol = ctx.SYMBOL().getText()
        if symbol in self.variables:
            sort = util.str_to_sort(self.variables[symbol])
            return z3.Const(symbol, sort)
        else:
            print("Invalid symbol found in visitSymbol_term: {}!".format(symbol))
            return z3.Const(symbol, z3.BoolSort())

    def visitLet_term_term(self, ctx:TermParser.Let_term_termContext):
        return self.visit(ctx.let_term())

    #def visitLet_term(self, ctx:TermParser.Let_termContext):
    #    res = Term('let', 'let_term')


class Rule_Extractor(TermVisitor):

    def visitFunc_g_term(self, ctx:TermParser.Func_g_termContext):
        g_terms = []
        for g_term in ctx.g_term():
            g_terms.append(g_term.getText())

        return [ctx.SYMBOL().getText(), *g_terms]        

    def visitLit_g_term(self, ctx:TermParser.Lit_g_termContext):
        return [ctx.literal().getText()]

    def visitSymbol_g_term(self, ctx:TermParser.Symbol_g_termContext):
        return [ctx.SYMBOL().getText()]
    
    # def visitLet_g_term_g_term(self, ctx:TermParser.Let_g_term_g_termContext):
    #     return self.visitChildren(ctx)

    # def visitConstant_g_term(self, ctx:TermParser.Constant_g_termContext):
    #     return self.visitChildren(ctx)

    # def visitVariable_g_term(self, ctx:TermParser.Variable_g_termContext):
    #     return self.visitChildren(ctx)

    # def visitInput_variable_g_term(self, ctx:TermParser.Input_variable_g_termContext):
    #     return self.visitChildren(ctx)

    # def visitLocal_variable_g_term(self, ctx:TermParser.Local_variable_g_termContext):
    #     return self.visitChildren(ctx)
    
    # def visitLet_g_term(self, ctx:TermParser.Let_g_termContext):
    #     return self.visitChildren(ctx)

