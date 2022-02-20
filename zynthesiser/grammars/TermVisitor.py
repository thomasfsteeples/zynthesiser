# Generated from Term.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .TermParser import TermParser
else:
    from TermParser import TermParser

# This class defines a complete generic visitor for a parse tree produced by TermParser.


class TermVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TermParser#nt_def.
    def visitNt_def(self, ctx: TermParser.Nt_defContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#func_term.
    def visitFunc_term(self, ctx: TermParser.Func_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#lit_term.
    def visitLit_term(self, ctx: TermParser.Lit_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#symbol_term.
    def visitSymbol_term(self, ctx: TermParser.Symbol_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#let_term_term.
    def visitLet_term_term(self, ctx: TermParser.Let_term_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#let_term.
    def visitLet_term(self, ctx: TermParser.Let_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#func_g_term.
    def visitFunc_g_term(self, ctx: TermParser.Func_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#lit_g_term.
    def visitLit_g_term(self, ctx: TermParser.Lit_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#symbol_g_term.
    def visitSymbol_g_term(self, ctx: TermParser.Symbol_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#let_g_term_g_term.
    def visitLet_g_term_g_term(self, ctx: TermParser.Let_g_term_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#constant_g_term.
    def visitConstant_g_term(self, ctx: TermParser.Constant_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#variable_g_term.
    def visitVariable_g_term(self, ctx: TermParser.Variable_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#input_variable_g_term.
    def visitInput_variable_g_term(self, ctx: TermParser.Input_variable_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#local_variable_g_term.
    def visitLocal_variable_g_term(self, ctx: TermParser.Local_variable_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#let_g_term.
    def visitLet_g_term(self, ctx: TermParser.Let_g_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#sort_expr.
    def visitSort_expr(self, ctx: TermParser.Sort_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#p_int_literal.
    def visitP_int_literal(self, ctx: TermParser.P_int_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#n_int_literal.
    def visitN_int_literal(self, ctx: TermParser.N_int_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#real_literal.
    def visitReal_literal(self, ctx: TermParser.Real_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#bool_literal.
    def visitBool_literal(self, ctx: TermParser.Bool_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#bv_literal.
    def visitBv_literal(self, ctx: TermParser.Bv_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#enum_literal.
    def visitEnum_literal(self, ctx: TermParser.Enum_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TermParser#enum_const.
    def visitEnum_const(self, ctx: TermParser.Enum_constContext):
        return self.visitChildren(ctx)


del TermParser
