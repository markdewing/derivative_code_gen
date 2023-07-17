from routine import Routine
from utils import routine_from_text
from codegen import (
    convert_routine_to_function,
    AltJuliaCodePrinter,
    AltCXX11CodePrinter,
)
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


def test_julia_codegen(debug=False):
    text1 = """
        e0 = 2*x**2 + 3*x
    """

    ref_text1 = """
function test1(x)
    e0 = 2 * x .^ 2 + 3 * x
    return e0
end
    """

    if debug:
        print("\nJulia codegen")

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R)

    printer = AltJuliaCodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)

    x = Symbol('x')
    dR = R.diff(x)
    dfunc = convert_routine_to_function(dR)
    ds = printer.doprint(dfunc)
    print(ds)


def test_python_codegen(debug=False):
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

    if debug:
        print("\nPython codegen")

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R)

    printer = PythonCodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)


def test_cpp_codegen(debug=False):
    text1 = """
        e0 = 2*x
        e1 = exp(-x)
    """

    ref_text1 = """
double test1(double x, double& e1){
   double e0;
   e0 = 2*x;
   e1 = std::exp(-x);
   return e0;
}
    """

    if debug:
        print("\nC++ codegen")

    R = routine_from_text("test1", text1)

    func = convert_routine_to_function(R, is_cpp=True)

    printer = AltCXX11CodePrinter()
    s = printer.doprint(func)
    if debug:
        print(s)
    compare_src(ref_text1, s)


if __name__ == "__main__":
    test_julia_codegen(debug=True)
    #test_python_codegen(debug=True)
    #test_cpp_codegen(debug=True)
