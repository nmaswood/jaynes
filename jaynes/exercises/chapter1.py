import jaynes.gate as gate

if __name__ == '__main__':

    A = gate.And(True, False)
    B = gate.And(True, False)

    C = gate.Or(gate.Nand(gate.Or(A, B), False), gate.Not(False))

    print(C.evaluate())

    res = gate.possible_truth_values(5)
    print (res)
