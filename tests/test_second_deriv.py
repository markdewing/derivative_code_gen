from sympy import symbols, Symbol
from routine import Routine, Statement
from utils import routine_from_text, compare_routines


# Compute second derivative only
def test_second_deriv_01(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*x
    """

    dtext2 = """
        e0 = 2*x**2 + 3*x
        e0_d2x = 4
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    if debug:
        print("Original function")
        R.print()
        print()

    R.debug = debug
    dR = R.diff((x, 2))

    if debug:
        print("Derivative function")
        dR.print()
        print()

    ref_dR = routine_from_text("test1_d2x", dtext2)
    compare_routines(ref_dR, dR)


# Compute first and second derivative
def test_second_deriv_02(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*x
    """

    dtext2 = """
        e0 = 2*x**2 + 3*x
        e0_d1x = 4*x + 3
        e0_d2x = 4
    """

    x = Symbol("x")
    R = routine_from_text("test2", text1)
    if debug:
        print("Original function")
        R.print()
        print()

    R.debug = debug
    dR = R.diff([x, (x, 2)])

    if debug:
        print("Derivative function")
        dR.print()
        print()

    ref_dR = routine_from_text("test2_d1x_d2x", dtext2)
    compare_routines(ref_dR, dR)


def test_second_deriv_03(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*x
    """

    dtext2 = """
        e0 = 2*x**2 + 3*x
        e0_d1x = 4*x + 3
        e0_d2x = 4
    """

    x = Symbol("x")
    R = routine_from_text("test2", text1)
    if debug:
        print("Original function")
        R.print()
        print()

    R.debug = debug
    dR = R.diff([x, (x, 2)])

    if debug:
        print("Derivative function")
        dR.print()
        print()

    ref_dR = routine_from_text("test2_d1x_d2x", dtext2)
    compare_routines(ref_dR, dR)


if __name__ == "__main__":
    # test_second_deriv_01(debug=True)
    test_second_deriv_02(debug=True)
