grammar Term;
import SyGuS_lexer_rules;

// Non-terminals

nt_def : LEFT_PARENS SYMBOL sort_expr LEFT_PARENS g_term+ RIGHT_PARENS RIGHT_PARENS ;

// Terms and grammar terms

term : LEFT_PARENS SYMBOL term* RIGHT_PARENS    # func_term
    | literal                                   # lit_term
    | SYMBOL                                    # symbol_term
    | let_term                                  # let_term_term
    ;

let_term : LEFT_PARENS 'let' LEFT_PARENS (LEFT_PARENS SYMBOL sort_expr term RIGHT_PARENS)+ RIGHT_PARENS term RIGHT_PARENS;

g_term : LEFT_PARENS SYMBOL g_term* RIGHT_PARENS            # func_g_term
    | literal                                               # lit_g_term
    | SYMBOL                                                # symbol_g_term
    | let_g_term                                            # let_g_term_g_term
    | LEFT_PARENS 'Constant' sort_expr RIGHT_PARENS         # constant_g_term
    | LEFT_PARENS 'Variable' sort_expr RIGHT_PARENS         # variable_g_term
    | LEFT_PARENS 'InputVariable' sort_expr RIGHT_PARENS    # input_variable_g_term
    | LEFT_PARENS 'LocalVariable' sort_expr RIGHT_PARENS    # local_variable_g_term
    ;

let_g_term : LEFT_PARENS 'let' LEFT_PARENS (LEFT_PARENS SYMBOL sort_expr g_term RIGHT_PARENS)+ RIGHT_PARENS g_term RIGHT_PARENS;

// Literals

sort_expr : 'Int' 
    | 'Bool'
    | 'Real'
    | LEFT_PARENS 'BitVec' POSITIVE_INT_CONST RIGHT_PARENS
    | LEFT_PARENS 'Enum' LEFT_PARENS SYMBOL+ RIGHT_PARENS RIGHT_PARENS
    | LEFT_PARENS 'Array' sort_expr sort_expr RIGHT_PARENS
    | SYMBOL
    ;

literal : POSITIVE_INT_CONST        # p_int_literal
    | NEGATIVE_INT_CONST            # n_int_literal
    | REAL_CONST                    # real_literal
    | BOOL_CONST                    # bool_literal
    | BV_CONST                      # bv_literal
    | enum_const                    # enum_literal
    ;

enum_const : SYMBOL '::' SYMBOL ;