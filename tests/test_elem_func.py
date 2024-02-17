from sympy import symbols, Symbol
from routine import Routine, Statement
from utils import compare_stmts, routine_from_text, stmts_from_text, compare_routines


def test_elem_func_01(debug=False):
    text1 = """
      e0 = exp(2*x)
      e1 = e0 + exp(-3*x)
    """

    dtext1 = """
      e0 = exp(2*x)
      e0_d1x = 2*exp(2*x)
      e1 = e0 + exp(-3*x)
      e1_d1x = e0_d1x + -3*exp(-3*x)
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)

    if debug:
        print("Original function")
        R.print()
        print()

    dR = R.diff(x)

    if debug:
        print("Derivative function")
        dR.print()
        print()

    ref_dR = routine_from_text("test1_d1arg0", dtext1)
    compare_routines(dR, ref_dR)


def test_elem_func_sqrt(debug=False):
    text1 = """
      e0 = sqrt(x*x + y*y + z*z)
    """

    dtext1 = """
      e0 = sqrt(x*x + y*y + z*z)
      e0_d1x = x/sqrt(x*x + y*y + z*z)
    """

    # x = Symbol("x")
    x, y, z = symbols("x y z")
    R = routine_from_text("test1", text1)
    # override the ordering of inputs from routine_from_text
    R.inputs = [x, y, z]

    if debug:
        print("Original function")
        R.print()
        print()

    dR = R.diff(x)

    if debug:
        print("Derivative function")
        dR.print()
        print()

    ref_dR = routine_from_text("test1_d1arg0", dtext1)
    ref_dR.inputs = [x, y, z]

    if debug:
        print("Reference derivative function")
        ref_dR.print()
        print()
    compare_routines(dR, ref_dR)


if __name__ == "__main__":
    test_elem_func_sqrt(debug=True)
