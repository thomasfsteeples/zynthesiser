import re
import z3

def is_int_literal(str):
    int_pattern = re.compile(r"^-?[0-9]+$")
    if int_pattern.match(str) is not None:
        return True
    else:
        return False

def is_real_literal(str):
    real_pattern = re.compile(r"^-?[0-9]+\.[0-9]+$")
    if real_pattern.match(str) is not None:
        return True
    else:
        return False   

def is_bool_literal(str):
    if str == 'true' or str == 'false':
        return True
    else:
        return False

def is_bv_literal(str):
    bv_pattern = re.compile(r"^(?:#b[01]+)|(?:#x[0-9a-f]+)$")
    if bv_pattern.match(str) is not None:
        return True
    else:
        return False

def is_symbol(str):
    symbol_pattern = re.compile(r"^[a-zA-Z_+\-*&|!~<>=/%?\.$\^][a-zA-Z_+\-*&|!~<>=/%?\.$\^0-9]*$")
    if symbol_pattern.match(str) is not None:
        return True
    else:
        return False

def str_to_sort(sort_str):
    z3_sort = z3.BoolSort()
    if sort_str == 'Bool':
        z3_sort = z3.BoolSort()
    elif sort_str == 'Int':
        z3_sort = z3.IntSort()
    elif sort_str == 'Real':
        z3_sort = z3.RealSort()
    else:
        bitvec_pattern = re.compile(r"^\(BitVec ([0-9]+)\)$")
        match = bitvec_pattern.match(sort_str)    
        if match != None:
            size = int(match.groups()[0])
            z3_sort = z3.BitVecSort(size)
        else:
            enum_pattern = re.compile(r"^\(Enum \( ((?:[a-zA-Z_+\-*&|!~<>=/%?\.$\^][a-zA-Z_+\-*&|!~<>=/%?\.$\^0-9]* )+)\)\)$")
            match = enum_pattern.match(sort_str)
            if match != None:
                values = match.groups()[0].strip()
                z3_sort = z3.EnumSort("Enum( {} )".format(values), values.split())
            # else:
            #     array_pattern = re.compile

    return z3_sort
        
def find_function_arguments(test_expr, f):
    subs = []
    if test_expr.decl().name() == f.name():
        subs.append(tuple(test_expr.children()))
    for child in test_expr.children():
        subs.extend(find_function_arguments(child, f))
    return list(set(subs))

def substitute_function_for_expression(test_expr, f, params, subs_expr):
    subs = find_function_arguments(test_expr, f)
    res = test_expr
    for sub in subs:
        sub_params = list(zip(params, sub))
        expr = z3.substitute(subs_expr, sub_params)
        res = z3.substitute(res, (f(*sub), expr))
    return z3.simplify(res)