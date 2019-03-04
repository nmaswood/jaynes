# from abc import ABC
from typing import Union, cast
from dataclasses import dataclass


class Gate():

    def evaluate(self):
        pass

    def compose(*args):
        pass


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
