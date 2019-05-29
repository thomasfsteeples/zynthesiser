lexer grammar SyGuS_lexer_rules;

LEFT_PARENS : '(' ;

RIGHT_PARENS : ')' ;

SYMBOL : (LOWERCASE_LETTER | UPPERCASE_LETTER | SPECIAL_CHAR) (LOWERCASE_LETTER | UPPERCASE_LETTER | DIGIT | SPECIAL_CHAR)* ;

QUOTED_LITERAL : '"' (LOWERCASE_LETTER | UPPERCASE_LETTER | DIGIT | '.')+ '"' ;

POSITIVE_INT_CONST : DIGIT+ ;

NEGATIVE_INT_CONST : '-' DIGIT+ ;

REAL_CONST : '-'? DIGIT+ '.' DIGIT+ ;

BOOL_CONST : 'true'
    | 'false'
    ;

BV_CONST : '#b'BINARY_DIGIT+
    | '#x' (DIGIT | HEXADECIMAL_DIGIT)+
    ;

COMMENT : ';' .*? '\r'?'\n' -> skip;

WHITESPACE : [ \t]+ -> skip;

NEWLINE : '\r'?'\n' -> skip;

// Fragment rules

fragment LOWERCASE_LETTER : [a-z] ;

fragment UPPERCASE_LETTER : [A-Z] ;

fragment SPECIAL_CHAR : [_+\-*&|!~<>=/%?.$^] ;

fragment DIGIT : [0-9] ;

fragment BINARY_DIGIT : [01] ;

fragment HEXADECIMAL_DIGIT : [a-fA-F] ;