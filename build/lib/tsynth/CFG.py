from collections import defaultdict
from copy import deepcopy
import z3

from tsynth.string_z3_conversion import expr_string_to_z3, z3_to_expr_string

# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
def flatten(list_of_lists):
    it = iter(list_of_lists)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in flatten(e):
                yield f
        else:
            yield e

class CFG:
    def __init__(self, rules):
        self.rules = rules
        self.start_symbol = list(self.rules.keys())[0]

        self.symbol_history = self.all_values()

    def non_terminals(self):
        return set(self.rules.keys())

    def all_values(self):
        return set(flatten(self.rules.values()))

    def terminals(self):
        return self.all_values().difference(self.non_terminals())

    def size(self):
        return len(list(flatten(self.rules.values())))

    def _find_symbol_not_in_grammar(self, start_letter, excluded = []):
        i = 0
        while True:
            candidate = start_letter + str(i)
            if candidate not in self.symbol_history and candidate not in excluded:
                self.symbol_history.add(candidate)
                return candidate
            else:
                i += 1

    def _find_multiple_symbols_not_in_grammar(self, start_letter, number):
        res = []
        for _ in range(number):
            res.append(self._find_symbol_not_in_grammar(start_letter, excluded=res))
        return res

    def add_rule(self, nt, rule):
        if nt in self.rules:
            self.rules[nt].append(rule)
        else: 
            self.rules[nt] = [rule]

    # Convert to Chomsky normal form
    def convert_to_chomsky_normal_form(self):
        new_grammar = deepcopy(self)

        # START
        new_start_symbol = new_grammar._find_symbol_not_in_grammar("S")
        
        new_grammar.add_rule(new_start_symbol,  [new_grammar.start_symbol])
        new_grammar.start_symbol = new_start_symbol

        # TERM
        changed_terminals = {}
        for nt in new_grammar.non_terminals():
            for i, rule in enumerate(new_grammar.rules[nt]):
                if len(rule) > 1:
                    for j, sym in enumerate(rule):
                        if sym not in new_grammar.non_terminals():
                            if sym not in changed_terminals:
                                new_non_terminal = new_grammar._find_symbol_not_in_grammar('N')
                                changed_terminals[sym] = new_non_terminal
                                new_grammar.add_rule(new_non_terminal, [sym])
                            new_grammar.rules[nt][i][j] = changed_terminals[sym]


        # BIN
        for nt in new_grammar.non_terminals():
            for i, rule in enumerate(new_grammar.rules[nt]):
                if len(rule) > 2:
                    new_non_terminals = new_grammar._find_multiple_symbols_not_in_grammar('A', len(rule)-2)
                    new_grammar.rules[nt][i] = [rule[0], new_non_terminals[0]]
                    for j in range(len(new_non_terminals[0:-1])):
                         new_grammar.add_rule(new_non_terminals[j], [rule[j+1], new_non_terminals[j+1]])
                    new_grammar.add_rule(new_non_terminals[-1], [rule[-2], rule[-1]])

        # DEL
        # Don't think I need this for time being?

        # UNIT
        removed_symbols = []
        for nt in new_grammar.non_terminals():
            for i, rule in enumerate(new_grammar.rules[nt]):
                if len(rule) == 1 and rule[0] in new_grammar.non_terminals():
                    del_symbol = rule[0]
                    del(new_grammar.rules[nt][i])
                    new_grammar.rules[nt].extend(new_grammar.rules[del_symbol])
                    removed_symbols.append(del_symbol)
                    for other_nt in new_grammar.non_terminals():
                        for j in range(len(new_grammar.rules[other_nt])):
                            for k in range(len(new_grammar.rules[other_nt][j])):
                                if new_grammar.rules[other_nt][j][k] == del_symbol:
                                    new_grammar.rules[other_nt][j][k] = nt

        for symbol in removed_symbols:
            del(new_grammar.rules[symbol])

        # Return
        return new_grammar

class Word_Generator:

        def __init__(self, cfg, logic, variables, constants):
            self.cfg = cfg.convert_to_chomsky_normal_form()
            self.memory = {}
            for nt in self.cfg.non_terminals():
                self.memory[nt] = {}

            self.logic = logic
            self.variables = variables
            self.constants = []

            self.original_non_terminals = cfg.non_terminals()
            self.original_non_terminals.add(self.cfg.start_symbol)

            self.unit_productions = {}
            for nt in self.cfg.rules:
                self.unit_productions[nt] = list(flatten(filter(lambda l: len(l) == 1, self.cfg.rules[nt])))

            self.product_productions = {}
            for nt in self.cfg.rules:
                self.product_productions[nt] = list(filter(lambda l: len(l) == 2, self.cfg.rules[nt]))

        def generate(self, from_symbol, word_length):
            if word_length == 1:
                return self.unit_productions[from_symbol]

            elif word_length in self.memory[from_symbol]:
                return self.memory[from_symbol][word_length]
    
            else:
                res = []
                for nt1, nt2 in self.product_productions[from_symbol]:
                    for i in range(1, word_length):
                            nt1_words = self.generate(nt1, i)
                            nt2_words = self.generate(nt2, word_length - i)
                            words = ["{} {}".format(w1, w2) for w1 in nt1_words for w2 in nt2_words]
                            res.extend(words)

                if from_symbol in self.original_non_terminals:        
                    simplified_res = set()

                    for word in res:
                        z3_expr = z3.simplify(expr_string_to_z3(word, self.logic, self.variables, self.constants))
                        simplified_word = z3_to_expr_string(z3_expr, self.logic, self.variables, self.constants)
                        simplified_res.add(simplified_word)

                    for i in range(1, word_length):
                        simplified_res -= set(self.generate(from_symbol, i))

                    simplified_res = list(simplified_res)
                    self.memory[from_symbol][word_length] = simplified_res
                    return simplified_res

                else:
                    self.memory[from_symbol][word_length] = res
                    return res
