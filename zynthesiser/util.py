import re
import z3
from .error import ZynthesiserException


def is_int_literal(s: str):
    int_pattern = re.compile(r"^-?[0-9]+$")
    if int_pattern.match(s) is not None:
        return True
    else:
        return False


def is_real_literal(s: str):
    real_pattern = re.compile(r"^-?[0-9]+\.[0-9]+$")
    if real_pattern.match(s) is not None:
        return True
    else:
        return False


def is_bool_literal(s: str):
    if s == "true" or s == "false":
        return True
    else:
        return False


def is_bv_literal(s: str):
    bv_pattern = re.compile(r"^(?:#b[01]+)|(?:#x[0-9a-fA-F]+)$")
    if bv_pattern.match(s) is not None:
        return True
    else:
        return False


def is_symbol(s: str):
    symbol_pattern = re.compile(
        r"^[a-zA-Z_+\-*&|!~<>=/%?\.$\^][a-zA-Z_+\-*&|!~<>=/%?\.$\^0-9]*$"
    )
    if symbol_pattern.match(s) is not None:
        return True
    else:
        return False


def str_to_sort(sort_str: str):
    if sort_str == "Bool":
        return z3.BoolSort()
    if sort_str == "Int":
        return z3.IntSort()
    if sort_str == "Real":
        return z3.RealSort()
    
    bitvec_pattern = re.compile(r"^\(BitVec ([0-9]+)\)$")
    match = bitvec_pattern.match(sort_str)
    if match is not None:
        size = int(match.groups()[0])
        return z3.BitVecSort(size)
    
    enum_pattern = re.compile(
                r"^\(Enum \( ((?:[a-zA-Z_+\-*&|!~<>=/%?\.$\^][a-zA-Z_+\-*&|!~<>=/%?\.$\^0-9]* )+)\)\)$"
            )
    match = enum_pattern.match(sort_str)
    if match is not None:
        values = match.groups()[0].strip()
        return z3.EnumSort("Enum( {} )".format(values), values.split())

    raise ZynthesiserException(f"str_to_sort: unrecognised sort: {sort_str}")


def contains_func(expr, func):
    if expr.decl().eq(func):
        return True
    else:
        for child in expr.children():
            if contains_func(child, func):
                return True
    return False


def contains_funcs(expr, funcs):
    for func in funcs:
        if contains_func(expr, func):
            return func
    return None


def find_function_arguments(expr, f):
    subs = []
    if expr.decl().name() == f.name():
        subs.append(tuple(expr.children()))
    for child in expr.children():
        subs.extend(find_function_arguments(child, f))
    return list(set(subs))


def substitute_function_for_expression(expr, f, params, subs_expr):
    subs = find_function_arguments(expr, f)
    res = expr
    for sub in subs:
        sub_params = list(zip(params, sub))
        expr = z3.substitute(subs_expr, sub_params)
        res = z3.substitute(res, (f(*sub), expr))
    return z3.simplify(res)
