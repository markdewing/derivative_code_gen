from sympy import symbols, Symbol
from routine import Routine, Statement


def routine_test_01():
    R = Routine("test1")
    x = Symbol("x")
    e1 = Symbol("e1")
    R.inputs = [x]
    R.outputs = [e1]
    R.stmts = [Statement(e1, 2 * x ** 2 + 3 * x)]

    R.print()

    R.debug = True
    dR = R.diff(x)
    print("Derivative function")
    dR.print()


def routine_test_02():
    R = Routine("test2")
    x = Symbol("x")
    e1 = Symbol("e1")
    e2 = Symbol("e2")
    R.inputs = [x]
    R.outputs = [e2]
    R.stmts = [Statement(e1, 2 * x ** 2 + 3 * x), Statement(e2, 3 * e1 + 4 * x)]

    R.print()

    R.debug = True
    dR = R.diff(x)
    print("Derivative function")
    dR.print()


print("Example 2 test 01")
routine_test_01()
print()
print("Example 2 test 02")

routine_test_02()
