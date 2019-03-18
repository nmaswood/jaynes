from dataclasses import dataclass
from itertools import combinations
from typing import List, Tuple, Union, cast


class Gate():
    def evaluate(self) -> bool:
        raise NotImplementedError


GateInput = Union[Gate, bool]


def _recurse(input_gate) -> bool:
    if type(input_gate) == bool:
        return cast(bool, input_gate)
    return cast(Gate, input_gate).evaluate()


@dataclass
class And(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return _recurse(self.A) and _recurse(self.B)


@dataclass
class Or(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return _recurse(self.A) or _recurse(self.B)


@dataclass
class Not(Gate):
    A: GateInput

    def evaluate(self) -> bool:
        return not _recurse(self.A)


@dataclass
class Nand(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return not And(self.A, self.B).evaluate()


@dataclass
class Nor(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return not Or(self.A, self.B).evaluate()


@dataclass
class Xor(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return bool(_recurse(self.A) ^ _recurse(self.B))


def possible_truth_values(n: int) -> List[Tuple[bool]]:
    init_set = [[True], [False]]

    for i in range(n - 1):
        result_set = []

        for value in init_set:
            for truth_value in [True, False]:
                value_prime = list(value + [truth_value])
                result_set.append(value_prime)
        init_set = result_set
    return result_set
