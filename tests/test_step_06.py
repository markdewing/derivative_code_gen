from sympy import Symbol, IndexedBase
from utils import routine_from_text
from codegen import (
    convert_routine_to_function,
    AltJuliaCodePrinter,
    AltCXX11CodePrinter,
    AltPythonCodePrinter,
)


def test_mag(debug=False):
    text = """
        mag = sqrt(r[0]*r[0] + r[1]*r[1] + r[2]*r[2])
    """
    r = IndexedBase("r", 3)

    ns = {"r": r}

    # r = Symbol('R')
    mag = routine_from_text("mag", text, local_vars=ns)
    if debug:
        print("Function")
        mag.print()

    if debug:
        print("Taking derivative")
    mag.debug = debug
    dmag = mag.diff(r)
    if debug:
        print("Derivative function")
        dmag.print()

    func = convert_routine_to_function(mag)
    dfunc = convert_routine_to_function(dmag)

    jprinter = AltJuliaCodePrinter()
    s = jprinter.doprint(func)
    ds = jprinter.doprint(dfunc)
    if debug:
        print("Julia function")
        print(s)
        print("Julia derivative function")
        print(ds)

    pprinter = AltPythonCodePrinter()
    s = pprinter.doprint(func)
    ds = pprinter.doprint(dfunc)
    if debug:
        print("Python function")
        print(s)
        print("Python derivative function")
        print(ds)

    cprinter = AltCXX11CodePrinter()
    s = cprinter.doprint(func)
    ds = cprinter.doprint(dfunc)
    if debug:
        print("C++ function")
        print(s)
        print("C++ derivative function")
        print(ds)


if __name__ == "__main__":
    test_mag(debug=True)
