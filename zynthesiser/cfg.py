from dataclasses import dataclass
from typing import Dict, List, Set, Union
from .error import ZynthesiserException

@dataclass(frozen=True)
class Nonterminal:
    val: str


@dataclass(frozen=True)
class Terminal:
    val: str


Symbol = Union[Nonterminal, Terminal]


class CFG:

    def __init__(self, productions: Dict[str, List[str]], start_symbol: str):
        self.nonterminals = set()
        for nt in productions.keys():
            self.nonterminals.add(Nonterminal(nt))
        
        self.start_symbol = Nonterminal(start_symbol)
        if self.start_symbol not in self.nonterminals:
            raise ZynthesiserException(f"zynthesiser.CFG: provided start_symbol {start_symbol} does not have corresponding production")
        
        self.memory = {}
        for nt in self.nonterminals:
            self.memory[nt] = {}
        

    def generate_words(self, nonterminal: Nonterminal, length: int):
        if length in self.memory[nonterminal]:
            return self.memory[nonterminal][length]
        res = []
        for prod in self.productions:
            partitions = ordered_partitions(length, len(prod))
            for part in partitions:
                generate_words(prod, part)
                res.extend(words)

        self.memory[nonterminal][length] = res
        return res
