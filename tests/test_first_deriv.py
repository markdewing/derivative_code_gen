from sympy import symbols, Symbol
from routine import Routine, Statement
from utils import compare_stmts, routine_from_text, stmts_from_text, compare_routines


def test_first_derivative_01(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*x
      e1 = 2*e0 + 3*e0**2
    """

    dtext1 = """
        e0 = 2*x**2 + 3*x
        e0_d1x = 4*x + 3
        e1 = 2*e0 + 3*e0**2
        e1_d1x = 2*e0_d1x*(3*e0 + 1)
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


def test_first_derivative_02(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*x
      e1 = 2*e0 + 3*e0**2
      e2 = 3*e1**2 + 4*x**3
    """

    dtext1 = """
        e0 = 2*x**2 + 3*x
        e0_d1x = 4*x + 3
        e1 = 2*e0 + 3*e0**2
        e1_d1x = 2*e0_d1x*(3*e0 + 1)
        e2 = 3*e1*e1 + 4*x**3
        e2_d1x =  6*e1*e1_d1x + 12*x**2
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


# Multiple input variables
def test_first_derivative_03(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*y
      e1 = 2*e0 + y*x
      e2 = 3*e1**2 + 4*x**3
    """

    dtext1 = """
        e0 = 2*x**2 + 3*y
        e0_d1x = 4*x
        e1 = 2*e0 + y*x
        e1_d1x = 2*e0_d1x + y
        e2 = 3*e1**2 + 4*x**3
        e2_d1x =  6*e1*e1_d1x + 12*x**2 
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


# Multiple input variables and multiple first derivatives
def test_first_derivative_03(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*y
      e1 = 2*e0 + y*x
      e2 = 3*e1**2 + 4*x**3
    """

    dtext1 = """
        e0 = 2*x**2 + 3*y
        e0_d1x = 4*x
        e0_d1y = 3
        e1 = 2*e0 + y*x
        e1_d1x = 2*e0_d1x + y
        e1_d1y = 2*e0_d1y + x
        e2 = 3*e1**2 + 4*x**3
        e2_d1x =  6*e1*e1_d1x + 12*x**2 
        e2_d1y =  6*e1*e1_d1y
    """

    x = Symbol("x")
    y = Symbol("y")
    R = routine_from_text("test1", text1)

    if debug:
        print("Original function")
        R.print()
        print()

    R.debug = debug
    dR = R.diff([x, y])

    if debug:
        print("Derivative function")
        dR.print()
        print()

    ref_dR = routine_from_text("test1_d1arg0_d1arg1", dtext1)

    if debug:
        print("Reference derivative function")
        ref_dR.print()
        print()

    compare_routines(dR, ref_dR)


# Multiple input variables and mixed derivatives
def test_first_derivative_04(debug=False):
    text1 = """
      e0 = 2*x**2 + 3*y
      e1 = 2*e0 + y*x
      e2 = 3*e1**2 + 4*x**3
    """

    dtext1 = """
        e0 = 2*x**2 + 3*y
        e0_d1y = 3
        e0_d1x = 4*x
        e1 = 2*e0 + y*x
        e1_d1y = 2*e0_d1y + x
        e1_d1x = 2*e0_d1x + y
        e1_d1x_d1y = 1
        e2 = 3*e1**2 + 4*x**3
        e2_d1y =  6*e1*e1_d1y
        e2_d1x =  6*e1*e1_d1x + 12*x**2 
        e2_d1x_d1y =  6*e1*e1_d1x_d1y + 6*e1_d1x*e1_d1y
    """

    x = Symbol("x")
    y = Symbol("y")
    R = routine_from_text("test1", text1)

    if debug:
        print("Original function")
        R.print()
        print()

    R.debug = debug
    dR_x = R.diff(x)
    dR_x.debug = debug
    dR_y = dR_x.diff(y)

    if debug:
        print("Derivative function")
        dR_y.print()
        print()

    ref_dR = routine_from_text("test1_d1arg0_d1arg1", dtext1)

    if debug:
        print("Reference derivative function")
        ref_dR.print()
        print()

    compare_routines(dR_y, ref_dR)


if __name__ == "__main__":
    # test_first_derivative_01(debug=True)
    # test_first_derivative_03(debug=True)
    test_first_derivative_04(debug=True)
