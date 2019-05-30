import z3
from inspect import getfullargspec
from tsynth.Symbol_Mapper import Symbol_Mapper
import re
import tsynth.util as util

import sys

def z3_to_expr_string(expr, logic, variables, constants):
    symbol_table = Symbol_Mapper.get_symbols_from_logic(logic)

    symbol = expr.decl().name()
    if len(expr.children()) > 0:
        children = []
        for child in expr.children():
            children.append(z3_to_expr_string(child, logic, variables, constants))

        arity = expr.decl().arity()
        return (symbol_table[symbol] + ' ')*(len(children) - arity + 1) + ' '.join(children)
    else:
        if symbol in variables or symbol in constants:
            return symbol
        elif symbol == 'Int':
            return expr.params()[0]
        elif symbol == 'true' or symbol == 'false':
            return symbol
        else:
            print('z3_to_expr_string is doing something weird - sort it out')
            print(symbol)

def expr_string_to_z3(expr_str, logic, variables, constants):

    eval_stack = []
    count_stack = []

    symbol_table = Symbol_Mapper.get_functions_from_logic(logic)

    tokens = expr_str.split(" ")
    for token in tokens:
        if token in symbol_table:
            arg_spec = getfullargspec(symbol_table[token])
            if arg_spec[3] != None:
                num_default_args = len(arg_spec[3])
            else:
                num_default_args = 0
            num_args = len(arg_spec[0]) - num_default_args
            eval_stack.append(symbol_table[token])
            count_stack.append([num_args, num_args])
        else:
            if util.is_int_literal(token):
                eval_stack.append(z3.IntVal(token))
            elif util.is_real_literal(token):
                eval_stack.append(z3.RealVal(token))
            elif util.is_bool_literal(token):
                eval_stack.append(z3.BoolVal(token))
            elif util.is_bv_literal(token):
                if token[:2] == '#x':
                    lit = int(token[2:], 16)
                    width = len(token[2:]) * 4
                else:
                    lit = int(token[2:], 2)
                    width = len(token[2:])
                eval_stack.append(z3.BitVecVal(lit, width))
            elif util.is_symbol(token):
                token_type = util.str_to_sort(variables[token])
                eval_stack.append(z3.Const(token, token_type))
            else:
                print("expr_string_to_z3 - odd token found: {}, something's gone wrong!".format(token))

            if len(count_stack) != 0:
                count_stack[-1][1] -= 1
                while len(count_stack) != 0 and count_stack[-1][1] == 0:
                    num_args = count_stack.pop()[0]

                    args = eval_stack[-num_args:]
                    eval_stack = eval_stack[:-num_args]

                    f = eval_stack.pop()
                    eval_stack.append(f(*args))
                    if len(count_stack) != 0:
                        count_stack[-1][1] -= 1

    return eval_stack[0]
