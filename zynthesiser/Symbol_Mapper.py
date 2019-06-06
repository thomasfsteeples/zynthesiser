from abc import ABCMeta, abstractmethod
import z3

class Symbol_Mapper(metaclass = ABCMeta):
    _theory_z3_to_expr_str_mapping = {

        'Core' : {
            # Boolean operators
            'not'       : 'not',
            '=>'        : '=>',
            'and'       : 'and', 
            'or'        : 'or',
            'xor'       : 'xor',
            # Polymorphic operators
            '='         : '=',
            'distinct'  : 'distinct',
            'if'        : 'ite'
        },

        'Ints' : {
            '#'         : '#', 
            '-'         : '-', 
            '+'         : '+', 
            '*'         : '*',
            'div'       : 'div',
            'mod'       : 'mod',

            '<='        : '<=',
            '<'         : '<',
            '>='        : '>=',
            '>'         : '>'
        },

        'FixedSizeBitVectors' : {
            'bvnot'     : 'bvnot',
            'bvneg'     : 'bvneg',
            'bvand'     : 'bvand',
            'bvor'      : 'bvor',
            'bvxor'     : 'bvxor',

            'bvadd'     : 'bvadd',
            'bvmul'     : 'bvmul',
            'bvudiv'    : 'bvudiv',
            'bvurem'    : 'bvurem',

            'bvshl'     : 'bvshl',
            'bvlshr'    : 'bvlshr',

            'concat'    : 'concat',
            # not happy about this - should be '_ extract'
            'extract'   : 'extract'
        }
        
    }

    _theory_expr_str_to_z3_mapping = {

        'Core' : {
            # Boolean operators
            'not'       : (z3.Not, 1),
            '=>'        : (z3.Implies, 2),
            'and'       : (z3.And, 2), 
            'or'        : (z3.Or, 2), 
            'xor'       : (z3.Xor, 2),
            # Polymorphic operators
            '='         : (lambda x, y: x == y, 2),
            'distinct'  : (z3.Distinct, 2),
            'ite'       : (z3.If, 3)
        },

        'Ints' : {
            '#'         : (lambda x: -x, 1),
            '-'         : (lambda x, y: x - y, 2),
            '+'         : (lambda x, y: x + y, 2),
            '*'         : (lambda x, y: x * y, 2),
            'div'       : (lambda x, y: x / y, 2),
            'mod'       : (lambda x, y: x % y, 2),
            'abs'       : (lambda x: z3.If(x >= 0, x, -x), 1),

            '<='        : (lambda x, y: x <= y, 2),
            '<'         : (lambda x, y: x < y, 2),
            '>='        : (lambda x, y: x >= y, 2),
            '>'         : (lambda x, y: x > y, 2)
        },

        'FixedSizeBitVectors' : {
            'bvnot'     : (lambda x: ~x, 1),
            'bvneg'     : (lambda x: -x, 1),
            'bvand'     : (lambda x, y: x & y, 2),
            'bvor'      : (lambda x, y: x | y, 2),
            'bvxor'     : (lambda x, y: x ^ y, 2),

            'bvadd'     : (lambda x, y: x + y, 2),
            'bvsub'     : (lambda x, y: x - y, 2),
            'bvmul'     : (lambda x, y: x * y, 2),
            'bvudiv'    : (z3.UDiv, 2),
            'bvsdiv'    : (lambda x, y: x / y, 2),
            'bvurem'    : (z3.URem, 2),
            'bvsrem'    : (z3.SRem, 2),

            'bvshl'     : (lambda x, y: x << y, 2),
            'bvashr'    : (lambda x, y: x >> y, 2),
            'bvlshr'    : (z3.LShR, 2),

            'bvugt'     : (z3.UGT, 2),
            'bvuge'     : (z3.UGE, 2),
            'bvule'     : (z3.ULE, 2),
            'bvult'     : (z3.ULT, 2),

            'bvslt'     : (lambda x, y: x < y, 2),
            'bvsle'     : (lambda x, y: x <= y, 2),

            'concat'    : (z3.Concat, 2),
            'extract'   : (z3.Extract, 3)
        }
        
    }

    _logic_mapping = {

        'LIA' : {
            'Core',
            'Ints'
        },

        'BV' : {
            'Core',
            'FixedSizeBitVectors'
        }
    }

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def get_symbols_from_logic(cls, logic):
        symbol_table = {}

        for theory in Symbol_Mapper._logic_mapping[logic]:
            symbol_table.update(Symbol_Mapper._theory_z3_to_expr_str_mapping[theory])

        return symbol_table

    @classmethod
    def get_symbol_from_function(cls, symbol, logic):
        symbol_table = Symbol_Mapper.get_symbols_from_logic(logic)
        return symbol_table[symbol]

    @classmethod
    def get_functions_from_logic(cls, logic):
        symbol_table = {}

        for theory in Symbol_Mapper._logic_mapping[logic]:
            symbol_table.update(Symbol_Mapper._theory_expr_str_to_z3_mapping[theory])

        return symbol_table

    @classmethod
    def get_function_from_symbol(cls, symbol, logic):
        symbol_table = Symbol_Mapper.get_functions_from_logic(logic)
        return symbol_table[symbol]

        
        