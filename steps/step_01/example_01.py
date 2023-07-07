from sympy import symbols, Symbol
from routine import Routine, Statement


def routine_test_01():
    R = Routine("test1")
    x = Symbol("x")
    e1 = Symbol("e1")
    e2 = Symbol("e2")
    R.inputs = [x]
    R.outputs = [e2]
    R.stmts = [Statement(e1, 2 * x ** 2), Statement(e2, 3 * e1 + x)]

    R.print()


routine_test_01()
