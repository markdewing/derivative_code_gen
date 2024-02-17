from sympy import symbols, Symbol
from routine import Routine
from utils import routine_from_text, compare_routines


def test_step_05_routine_01(debug=False):
    text1 = """
      e0 = g(x)
    """

    dtext1 = """
        e0,tmp_e0_d1arg0 = g_d1arg0(x)
        e0_d1x = tmp_e0_d1arg0
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff(x)

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1arg0", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_dependency_01(debug=False):
    text1 = """
      e0 = g(x)
      e1 = 2*x + 3*e0
      e2 = 3*y
      e3 = h(e1,y)
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    deps, func_deps = R.build_dependencies(R.stmts)
    R.print_dependencies(R.stmts, deps, func_deps)


def test_step_05_routine_03(debug=False):
    text1 = """
      e0 = g(x)
      e1 = h(e0)
    """

    dtext1 = """
        e0,tmp_e0_d1arg0 = g_d1arg0(x)
        e0_d1x = tmp_e0_d1arg0
        e1,tmp_e1_d1arg0 = h_d1arg0(e0)
        e1_d1x = e0_d1x * tmp_e1_d1arg0
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff(x)

    if debug:
        print("-- dR -----")
        dR.print()
        print("-----------")

    ref_dR = routine_from_text("test1_d1arg0", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_routine_04(debug=False):
    text1 = """
      e0 = g(x,y)
    """

    dtext1 = """
        e0,tmp_e0_d1arg0,tmp_e0_d1arg1 = g_d1arg0_d1arg1(x,y)
        e0_d1x = tmp_e0_d1arg0
        e0_d1y = tmp_e0_d1arg1
    """

    x = Symbol("x")
    y = Symbol("y")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff([(x, 1), (y, 1)])

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1arg0_d1arg1", dtext1)
    compare_routines(ref_dR, dR)


# Skip handling the case of calling diff twice, for now.
def skip_test_step_05_routine_05(debug=False):
    text1 = """
      e0 = g(x,y)
    """

    dtext1 = """
        e0,tmp_e0_d1arg0 = g_d1arg0(x,y)
        e0_d1x = tmp_e0_d1arg0
    """

    dtext1b = """
        a,dh_darg0 = h(x,y)
        e1 = dh_darg0
    """

    dtext2 = """
        e0,tmp_e0_d1arg0,tmp_e0_d1arg1,tmp_tmp_e0_d1arg0_d1arg1 = g_d1arg0_d1arg1(x,y)
        e0_d1y = tmp_e0_d1arg1
        tmp_e0_d1arg0_d1y = tmp_tmp_e0_d1arg0_d1arg1
        e0_d1x = tmp_e0_d1arg0
        e0_d1x_d1y = tmp_e0_d1arg0_d1y
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


# Multiple function calls with different variables
def test_step_05_routine_06(debug=False):
    text1 = """
      e0 = g(x)
      e1 = g(y)
      e2 = e1*e1
    """

    dtext1 = """
        e0,tmp_e0_d1a1 = g_d1a1(x)
        e1,tmp_e1_d1a1 = g_d1a1(y)
        e0_d1x = tmp_e0_d1x
    """

    x = Symbol("x")
    y = Symbol("y")
    R = routine_from_text("test1", text1)
    R.debug = debug
    print("Diffing R wrt x and y")
    dR1 = R.diff([x, y])
    if debug:
        dR1.print()


# First and second derivative
def test_step_05_routine_07(debug=False):
    text1 = """
      e0 = g(x)
    """

    dtext1 = """
        e0,tmp_e0_d1arg0,tmp_e0_d2arg0 = g_d1arg0_d2arg0(x)
        e0_d1x = tmp_e0_d1arg0
        e0_d2x = tmp_e0_d2arg0
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff([x, (x, 2)])

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1arg0_d2arg0", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_routine_08(debug=False):
    text1 = """
      e0 = g(x**2)
    """

    dtext1 = """
        e0,tmp_e0_d1arg0,tmp_e0_d2arg0 = g_d1arg0_d2arg0(x**2)
        e0_d1x = tmp_e0_d1arg0 * 2 * x
        e0_d2x = tmp_e0_d2arg0 * 4 * x**2 + tmp_e0_d1arg0 * 2
    """

    x = Symbol("x")
    R = routine_from_text("test1", text1)
    R.debug = debug
    dR = R.diff([x, (x, 2)])

    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1arg0_d2arg0", dtext1)
    compare_routines(ref_dR, dR)


def test_step_05_routine_09(debug=False):
    text1 = """
      e0 = x - y
      e1 = f(e0)
    """

    dtext1 = """
      e0 = x - y
      e0_d1x = 1
      e0_d1y = -1
      e1, tmp_e1_d1arg0 = f_d1arg0(e0)
      e1_d1x = e0_d1x*tmp_e1_d1arg0
      e1_d1y = e0_d1y*tmp_e1_d1arg0
    """

    R = routine_from_text("test1", text1)
    R.debug = debug

    x, y = symbols("x y")
    dR = R.diff([x, y])
    if debug:
        dR.print()

    ref_dR = routine_from_text("test1_d1arg0_d1arg1", dtext1)
    compare_routines(ref_dR, dR)


if __name__ == "__main__":
    # test_step_05_dependency_01(debug=True)
    # test_step_05_routine_01(debug=True)
    # test_step_05_routine_03(debug=True)
    # test_step_05_routine_04(debug=True)
    # skip_test_step_05_routine_05(debug=True)
    # test_step_05_routine_06(debug=True)
    # test_step_05_routine_07(debug=True)
    # test_step_05_routine_08(debug=True)
    test_step_05_routine_09(debug=True)
