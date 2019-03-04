from typing import Union, cast
from dataclasses import dataclass


class Gate():
    def evaluate(self) -> bool:
        raise NotImplementedError


@dataclass
class GateInput:
    value: Union[Gate, bool]

    def recurse(self) -> bool:
        if type(self.value) == bool:
            return cast(bool, self.value)
        return cast(Gate, self.value).evaluate()


@dataclass
class And(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return self.A.recurse() and self.B.recurse()


@dataclass
class Or(Gate):
    A: GateInput
    B: GateInput

    def evaluate(self) -> bool:
        return self.A.recurse() or self.B.recurse()


@dataclass
class Not(Gate):
    A: GateInput

    def evaluate(self) -> bool:
        return not self.A.recurse()


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
        return bool(self.A.recurse() ^ self.B.recurse())
