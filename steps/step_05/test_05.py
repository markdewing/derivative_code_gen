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


if __name__ == "__main__":
    test_step_05_routine_01(debug=True)
