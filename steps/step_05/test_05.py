from sympy import symbols, Symbol
from routine import Routine
from utils import routine_from_text, compare_routines


def test_step_05_routine_01(debug=False):
    text1 = """
      e0 = g(x)
    """

    dtext1 = """
        e0,tmp_e0_d1x = g_d1x(x)
        e0_d1x = tmp_e0_d1x
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff(x)

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1x", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_routine_03(debug=False):
    text1 = """
      e0 = g(x)
      e1 = h(e0)
    """

    dtext1 = """
        e0,tmp_e0_d1x = g_d1x(x)
        e0_d1x = tmp_e0_d1x
        e1,tmp_e1_d1x = h_d1x(e0)
        e1_d1x = e0_d1x * tmp_e1_d1x 
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff(x)

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1x", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_routine_04(debug=False):
    text1 = """
      e0 = g(x,y)
    """

    dtext1 = """
        e0,tmp_e0_d1x,tmp_e0_d1y = g_d1x_d1y(x,y)
        e0_d1x = tmp_e0_d1x
        e0_d1y = tmp_e0_d1y
    """

    x = Symbol("x")
    y = Symbol("y")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff([(x, 1), (y, 1)])

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1x_d1y", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_routine_05(debug=False):
    text1 = """
      e0 = g(x,y)
    """

    dtext1 = """
        e0,tmp_e0_d1x = g_d1x(x,y)
        e0_d1x = tmp_e0_d1x
    """

    dtext2 = """
        e0,tmp_e0_d1x,tmp_e0_d1y,tmp_tmp_e0_d1x_d1y = g_d1x_d1y(x,y)
        e0_d1y = tmp_e0_d1y
        tmp_e0_d1x_d1y = tmp_tmp_e0_d1x_d1y
        e0_d1x = tmp_e0_d1x
        e0_d1x_d1y = tmp_e0_d1x_d1y
    """

    x = Symbol("x")
    y = Symbol("y")
    R = routine_from_text("test1", text1)
    R.debug = debug
    print("Diffing R wrt x")
    dR1 = R.diff(x)
    if debug:
        dR1.print()

    ref_dR1 = routine_from_text("test1_d1x", dtext1)
    compare_routines(ref_dR1, dR1)

    print("Diffing dR1 wrt y")
    dR1.debug = debug
    dR = dR1.diff(y)

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1x_d1y", dtext2)

    compare_routines(ref_dR, dR)


if __name__ == "__main__":
    # test_step_05_routine_01(debug=True)
    # test_step_05_routine_02(debug=True)
    # test_step_05_routine_03(debug=True)
    # test_step_05_routine_04(debug=True)
    test_step_05_routine_05(debug=True)
