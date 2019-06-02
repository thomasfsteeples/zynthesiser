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
            'not'       : z3.Not,
            '=>'        : z3.Implies,
            'and'       : z3.And, 
            'or'        : z3.Or, 
            'xor'       : z3.Xor,
            # Polymorphic operators
            '='         : lambda x, y: x == y,
            'distinct'  : z3.Distinct,
            'ite'       : z3.If,
        },

        'Ints' : {
            '#'         : lambda x: -x, 
            '-'         : lambda x, y: x - y, 
            '+'         : lambda x, y: x + y, 
            '*'         : lambda x, y: x * y,
            'div'       : lambda x, y: x / y,
            'mod'       : lambda x, y: x % y,
            'abs'       : lambda x: z3.If(x >= 0, x, -x),

            '<='        : lambda x, y: x <= y,
            '<'         : lambda x, y: x < y, 
            '>='        : lambda x, y: x >= y,
            '>'         : lambda x, y: x > y
        },

        'FixedSizeBitVectors' : {
            'bvnot'     : lambda x: ~x,
            'bvneg'     : lambda x: -x,
            'bvand'     : lambda x, y: x & y,
            'bvor'      : lambda x, y: x | y,
            'bvxor'     : lambda x, y: x ^ y,

            'bvadd'     : lambda x, y: x + y,
            'bvmul'     : lambda x, y: x * y,
            'bvudiv'    : z3.UDiv,
            'bvurem'    : z3.URem,

            'bvshl'     : lambda x, y: x << y,
            'bvlshr'    : z3.LShR,

            'concat'    : z3.Concat,
            'extract'   : z3.Extract
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

        
        