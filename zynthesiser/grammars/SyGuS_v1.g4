grammar SyGuS_v1;
import Term, SyGuS_lexer_rules;

// Each SyGuS-IF file contains a command which sets the logic,
// followed by a list of commands

sygus : set_logic_cmd cmd+
    | cmd+
    ;

cmd : sort_def_cmd
    | var_decl_cmd
    | fun_decl_cmd
    | fun_def_cmd
    | synth_fun_cmd
    | constraint_cmd
    | check_synth_cmd
    | set_opts_cmd
    ;

// Declaring the problem logic 

set_logic_cmd : LEFT_PARENS 'set-logic' SYMBOL RIGHT_PARENS ;

// Defining new sorts specific to the problem

sort_def_cmd : LEFT_PARENS 'define-sort' SYMBOL sort_expr RIGHT_PARENS ;

// Declaring universally quantified variables

var_decl_cmd : LEFT_PARENS 'declare-var' SYMBOL sort_expr RIGHT_PARENS ;

// Declare an unintepreted function

fun_decl_cmd : LEFT_PARENS 'declare-fun' SYMBOL LEFT_PARENS sort_expr* RIGHT_PARENS sort_expr LEFT_PARENS;

// Macros

fun_def_cmd : LEFT_PARENS 'define-fun' SYMBOL LEFT_PARENS (LEFT_PARENS SYMBOL sort_expr RIGHT_PARENS)* RIGHT_PARENS sort_expr term RIGHT_PARENS;

// Define syntheis functions

synth_fun_cmd : LEFT_PARENS 'synth-fun' SYMBOL LEFT_PARENS (LEFT_PARENS SYMBOL sort_expr RIGHT_PARENS)* RIGHT_PARENS sort_expr LEFT_PARENS nt_def+ RIGHT_PARENS RIGHT_PARENS ;

// Synthesis constraints

constraint_cmd : LEFT_PARENS 'constraint' term RIGHT_PARENS ;

// Initialise synthesis and synthesizer output

check_synth_cmd : LEFT_PARENS 'check-synth' RIGHT_PARENS ;

// Solver-specific options

set_opts_cmd : LEFT_PARENS 'set-options' LEFT_PARENS (LEFT_PARENS SYMBOL QUOTED_LITERAL RIGHT_PARENS)+ RIGHT_PARENS RIGHT_PARENS ;