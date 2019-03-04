import jaynes.gate as gate

if __name__ == '__main__':

    A = gate.And(True, False)
    B = gate.And(True, True)

    C = gate.Or(A, B)

    print(C.evaluate())
