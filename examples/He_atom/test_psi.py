from sympy import Symbol, IndexedBase
from utils import routine_from_text


def test_mag(debug=False):
    text = """
        mag = sqrt(r[0]*r[0] + r[1]*r[1] + r[2]*r[2])
    """
    r = IndexedBase('r',3)
    ns = {"r" : r}
    mag = routine_from_text("mag", text, local_vars=ns)
    mag.debug = debug
    dmag = mag.diff(r)
    if debug:
        mag.print()


def test_jastrow(debug=False):
    text = """
        A = 0.5
        e0 = exp(A*r/(1 + B*r))
    """
    r = Symbol("r")
    R = routine_from_text("jastrow", text)
    R.debug = debug
    dR = R.diff(r)
    if debug:
        dR.print()


def test_orb(debug=False):
    text = """
        Z = 2.0
        norm = 0.5/sqrt(pi)
        r_mag = mag(R)
        orb = norm*exp(-Z*r_mag)
    """
    # R = IndexedBase('R',3)
    R = Symbol("R")
    orb = routine_from_text("orb", text)
    orb.debug = debug
    dorb = orb.diff(R)
    if debug:
        orb.print()


def test_psi(debug=False):
    text = """
        o1 = orb(r1)
        o2 = orb(r2)
        r12 = r2 - r1
        r12_mag = mag(r12)
        j = jastrow(r12_mag, B)
        p = o1*o2*j
    """
    # r1 = IndexedBase('r1',3)
    # r2 = IndexedBase('r2',3)
    r1 = Symbol("r1")
    r2 = Symbol("r2")
    R = routine_from_text("psi", text)
    R.debug = debug
    dR = R.diff([r1, r2])
    if debug:
        dR.print()


if __name__ == "__main__":
    test_jastrow(debug=True)
    test_orb(debug=True)
    test_psi(debug=True)
    test_mag(debug=True)
