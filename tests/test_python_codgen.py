from routine import Routine
from utils import routine_from_text
from codegen import (
    convert_routine_to_function,
    AltJuliaCodePrinter,
    AltCXX11CodePrinter,
)
from codegen_utils import compare_src
from sympy.printing.pycode import PythonCodePrinter
from sympy.printing.cxx import CXX11CodePrinter
from sympy import Symbol


def test_python_codegen_01(debug=False):
    text1 = """
        e0 = 2*x
    """

    ref_text1 = """
def test1(x):
    e0 = 2*x
    return e0
    """

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R)

    printer = PythonCodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)


def test_python_codegen_02(debug=False):
    text1 = """
        e0 = 2*x
        e1 = exp(-x)
    """

    ref_text1 = """
    def test1(x):
      e0 = 2*x
      e1 = math.exp(-x)
      return (e0, e1)
    """

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R)

    printer = PythonCodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)


if __name__ == "__main__":
    test_python_codegen_02(debug=True)
