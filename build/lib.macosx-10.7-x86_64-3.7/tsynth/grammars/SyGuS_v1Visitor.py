# Generated from SyGuS_v1.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SyGuS_v1Parser import SyGuS_v1Parser
else:
    from SyGuS_v1Parser import SyGuS_v1Parser

# This class defines a complete generic visitor for a parse tree produced by SyGuS_v1Parser.

class SyGuS_v1Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by SyGuS_v1Parser#sygus.
    def visitSygus(self, ctx:SyGuS_v1Parser.SygusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#cmd.
    def visitCmd(self, ctx:SyGuS_v1Parser.CmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#set_logic_cmd.
    def visitSet_logic_cmd(self, ctx:SyGuS_v1Parser.Set_logic_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#sort_def_cmd.
    def visitSort_def_cmd(self, ctx:SyGuS_v1Parser.Sort_def_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#var_decl_cmd.
    def visitVar_decl_cmd(self, ctx:SyGuS_v1Parser.Var_decl_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#fun_decl_cmd.
    def visitFun_decl_cmd(self, ctx:SyGuS_v1Parser.Fun_decl_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#fun_def_cmd.
    def visitFun_def_cmd(self, ctx:SyGuS_v1Parser.Fun_def_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#synth_fun_cmd.
    def visitSynth_fun_cmd(self, ctx:SyGuS_v1Parser.Synth_fun_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#constraint_cmd.
    def visitConstraint_cmd(self, ctx:SyGuS_v1Parser.Constraint_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#check_synth_cmd.
    def visitCheck_synth_cmd(self, ctx:SyGuS_v1Parser.Check_synth_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#set_opts_cmd.
    def visitSet_opts_cmd(self, ctx:SyGuS_v1Parser.Set_opts_cmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#nt_def.
    def visitNt_def(self, ctx:SyGuS_v1Parser.Nt_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#func_term.
    def visitFunc_term(self, ctx:SyGuS_v1Parser.Func_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#lit_term.
    def visitLit_term(self, ctx:SyGuS_v1Parser.Lit_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#symbol_term.
    def visitSymbol_term(self, ctx:SyGuS_v1Parser.Symbol_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#let_term_term.
    def visitLet_term_term(self, ctx:SyGuS_v1Parser.Let_term_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#let_term.
    def visitLet_term(self, ctx:SyGuS_v1Parser.Let_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#func_g_term.
    def visitFunc_g_term(self, ctx:SyGuS_v1Parser.Func_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#lit_g_term.
    def visitLit_g_term(self, ctx:SyGuS_v1Parser.Lit_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#symbol_g_term.
    def visitSymbol_g_term(self, ctx:SyGuS_v1Parser.Symbol_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#let_g_term_g_term.
    def visitLet_g_term_g_term(self, ctx:SyGuS_v1Parser.Let_g_term_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#constant_g_term.
    def visitConstant_g_term(self, ctx:SyGuS_v1Parser.Constant_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#variable_g_term.
    def visitVariable_g_term(self, ctx:SyGuS_v1Parser.Variable_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#input_variable_g_term.
    def visitInput_variable_g_term(self, ctx:SyGuS_v1Parser.Input_variable_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#local_variable_g_term.
    def visitLocal_variable_g_term(self, ctx:SyGuS_v1Parser.Local_variable_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#let_g_term.
    def visitLet_g_term(self, ctx:SyGuS_v1Parser.Let_g_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#sort_expr.
    def visitSort_expr(self, ctx:SyGuS_v1Parser.Sort_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#p_int_literal.
    def visitP_int_literal(self, ctx:SyGuS_v1Parser.P_int_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#n_int_literal.
    def visitN_int_literal(self, ctx:SyGuS_v1Parser.N_int_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#real_literal.
    def visitReal_literal(self, ctx:SyGuS_v1Parser.Real_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#bool_literal.
    def visitBool_literal(self, ctx:SyGuS_v1Parser.Bool_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#bv_literal.
    def visitBv_literal(self, ctx:SyGuS_v1Parser.Bv_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#enum_literal.
    def visitEnum_literal(self, ctx:SyGuS_v1Parser.Enum_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SyGuS_v1Parser#enum_const.
    def visitEnum_const(self, ctx:SyGuS_v1Parser.Enum_constContext):
        return self.visitChildren(ctx)



del SyGuS_v1Parser