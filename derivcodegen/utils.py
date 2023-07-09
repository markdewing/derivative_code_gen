from sympy import sympify
from routine import Routine, Statement
from collections import OrderedDict


def stmts_from_text(text):
    # print('parsing from ',text)
    stmts = []
    for line in text.split("\n"):
        line = line.strip()
        # print("line = ",line)
        if not line:
            continue
        vals = line.split("=")
        # print("   vals = ",vals)
        if len(vals) == 2:
            lhs = sympify(vals[0])
            rhs = sympify(vals[1])
            stmts.append(Statement(lhs, rhs))
        else:
            print("unexpected length = ", len(vals), vals)

    return stmts


# Look for free symbols that are not assigned in any statements
def find_inputs(stmts):
    free_syms = set()
    ordered_syms = OrderedDict()
    for s in reversed(stmts):
        free_syms.update(s.rhs.free_symbols)
        for s1 in s.rhs.free_symbols:
            ordered_syms[s1] = None
        free_syms.discard(s.lhs)

    used_syms_ordered = list()
    for s in ordered_syms.keys():
        if s in free_syms:
            used_syms_ordered.append(s)
    return used_syms_ordered


# Look for assigned symbols that are not used in any other statements
def find_outputs(stmts):
    unused_syms = set()
    ordered_syms = OrderedDict()
    for s in stmts:
        unused_syms.add(s.lhs)
        ordered_syms[s.lhs] = None
        unused_syms.difference_update(s.rhs.free_symbols)

    unused_syms_ordered = list()
    for s in ordered_syms.keys():
        if s in unused_syms:
            unused_syms_ordered.append(s)

    return unused_syms_ordered


def routine_from_text(name, text):
    R = Routine(name)
    R.stmts = stmts_from_text(text)
    inps = find_inputs(R.stmts)
    R.inputs = list(inps)
    outs = find_outputs(R.stmts)
    R.outputs = list(outs)
    return R


def compare_stmts(stmts1, stmts2):
    assert len(stmts1) == len(stmts2)
    for s1, s2 in zip(stmts1, stmts2):
        assert s1 == s2, str(s1) + " versus " + str(s2)


def compare_routines(r1, r2):
    assert r1.name == r2.name

    assert len(r1.inputs) == len(r2.inputs)
    for i1, i2 in zip(sorted(r1.inputs, key=str), sorted(r2.inputs, key=str)):
        assert i1 == i2

    assert len(r1.outputs) == len(r2.outputs)
    for o1, o2 in zip(sorted(r1.outputs, key=str), sorted(r2.outputs, key=str)):
        assert o1 == o2, "Output: " + str(o1) + " != " + str(o2)

    compare_stmts(r1.stmts, r2.stmts)
