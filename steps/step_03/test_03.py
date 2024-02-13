from sympy import symbols, Symbol
from routine import Routine, Statement, normalize_variable_list, variable_deriv_name
from utils import compare_stmts, routine_from_text, stmts_from_text, compare_routines


# Manually constructed test case
def test_step_03_routine_01():
    R = Routine("test1")
    x = Symbol("x")
    e1 = Symbol("e1")
    R.inputs = [x]
    R.outputs = [e1]
    R.stmts = [Statement(e1, 2 * x ** 2 + 3 * x)]

    dR = R.diff(x)

    e1_d1x = Symbol("e1_d1x")
    ref_dR = Routine("test1_d1x")
    ref_dR.inputs = [x]
    ref_dR.outputs = [e1, e1_d1x]
    ref_dR.stmts = [Statement(e1, 2 * x ** 2 + 3 * x), Statement(e1_d1x, 4 * x + 3)]

    assert ref_dR.name == dR.name
    assert ref_dR.inputs == dR.inputs
    assert ref_dR.outputs == dR.outputs
    compare_stmts(ref_dR.stmts, dR.stmts)


# Test case using string inputs
def test_step_03_routine_02():
    text1 = """
      e0 = 2*x**2 + 3*x
    """

    dtext1 = """
        e0 = 2*x**2 + 3*x
        e0_d1x = 4*x + 3
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    dR = R.diff(x)

    ref_dR = routine_from_text("test1_d1x", dtext1)
    compare_routines(dR, ref_dR)


def test_normalize_var_list():
    x = Symbol("x")
    y = Symbol("y")
    v1 = normalize_variable_list(x)
    assert v1 == [(x, 1)]

    v2 = normalize_variable_list([x, y])
    assert v2 == [(x, 1), (y, 1)]

    v3 = normalize_variable_list([x, (x, 2), (y, 1)])
    assert v3 == [(x, 1), (x, 2), (y, 1)]


def test_variable_deriv_name():
    x = Symbol("x")
    name = variable_deriv_name("base", x, 1)
    assert name == "base_d1x"
