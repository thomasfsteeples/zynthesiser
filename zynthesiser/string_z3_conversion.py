import re
import sys
from inspect import getfullargspec

import z3

import zynthesiser.util as util
from zynthesiser.Symbol_Mapper import Symbol_Mapper


def z3_to_expr_string(expr, spec, variables_in_scope):
    symbol_table = Symbol_Mapper.get_symbols_from_logic(spec.logic)

    symbol = expr.decl().name()
    z3_children = expr.children()
    if len(z3_children) > 0:
        children = []
        for child in z3_children:
            children.append(z3_to_expr_string(child, spec, variables_in_scope))

        params = []
        z3_params = expr.params()
        for param in z3_params:
            params.append(str(param))

        if symbol in symbol_table:
            f = symbol_table[symbol]
        else:
            f = symbol

        arity = expr.decl().arity()

        if len(params) > 0:
            return (
                (f + " ") * (len(children) - arity + 1)
                + " ".join(params)
                + " "
                + " ".join(children)
            )
        else:
            return (f + " ") * (len(children) - arity + 1) + " ".join(children)

    else:
        if symbol in variables_in_scope:
            return symbol
        else:
            if z3.is_int(expr):
                return expr.params()[0]
            elif z3.is_bool(expr):
                return symbol
            elif z3.is_bv(expr):
                num_str, size = expr.params()
                num = int(num_str)
                hex_num = hex(num)[2:]
                padded_hex_num = "0" * (size // 4 - len(hex_num)) + hex_num
                return "#x{}".format(padded_hex_num)
            else:
                print("z3_to_expr_string is doing something weird - sort it out")
                print(symbol)


def expr_string_to_z3(expr_str, spec, variables_in_scope):

    eval_stack = []
    count_stack = []

    symbol_table = Symbol_Mapper.get_functions_from_logic(spec.logic)

    tokens = expr_str.split(" ")
    for token in tokens:
        # Handle functions first
        if token in symbol_table:
            num_args = symbol_table[token][1]
            eval_stack.append(symbol_table[token][0])
            count_stack.append([num_args, num_args])

        elif token in spec.uninterpreted_funcs:
            func = spec.uninterpreted_funcs[token]["decl"]
            num_args = func.arity()
            eval_stack.append(func)
            count_stack.append([num_args, num_args])

        elif token in spec.macros:
            func = spec.macros[token]["decl"]
            num_args = func.arity()
            eval_stack.append(func)
            count_stack.append([num_args, num_args])

        # Now handle literals and variables
        else:
            if util.is_int_literal(token):
                eval_stack.append(z3.IntVal(token))
            elif util.is_real_literal(token):
                eval_stack.append(z3.RealVal(token))
            elif util.is_bool_literal(token):
                eval_stack.append(z3.BoolVal(token))
            elif util.is_bv_literal(token):
                if token[:2] == "#x":
                    lit = int(token[2:], 16)
                    width = len(token[2:]) * 4
                else:
                    lit = int(token[2:], 2)
                    width = len(token[2:])
                eval_stack.append(z3.BitVecVal(lit, width))
            elif util.is_symbol(token):
                token_type = util.str_to_sort(variables_in_scope[token])
                eval_stack.append(z3.Const(token, token_type))
            else:
                import pdb

                pdb.set_trace()
                print(
                    "expr_string_to_z3 - odd token found: {}, something's gone wrong!".format(
                        token
                    )
                )

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
