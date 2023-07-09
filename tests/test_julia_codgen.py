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


def make_lines(text):
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return lines


def compare_src(s1, s2):
    ln1 = make_lines(s1)
    ln2 = make_lines(s2)
    for (l1, l2) in zip(ln1, ln2):
        assert l1 == l2, l1 + " versus " + l2


def test_julia_codegen_01(debug=False):
    text1 = """
        e0 = 2*x
    """

    ref_text1 = """
function test1(x)
    e0 = 2 * x
    return e0
end
    """

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R)

    printer = AltJuliaCodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)


def test_julia_codegen_02(debug=False):
    text1 = """
        e0 = 2*x
        e1 = exp(-x)
    """

    ref_text1 = """
function test1(x)
    e0 = 2 * x
    e1 = exp(-x)
    return (e0, e1)
end
    """

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R)

    printer = AltJuliaCodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)


if __name__ == "__main__":
    test_julia_codegen_02(debug=True)
