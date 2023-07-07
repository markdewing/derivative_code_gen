
## Third step - testing

Now that there is some code, we should set up some testing.
For constructing tests, it would be convenient to have a simple text representation of the statements.
For this purpose, we implement some utility functions to perform that conversion and to extract the inputs (free symbols)
and the outputs (symbols unused by other statements)


The manual construction of a routine:
```
    x = Symbol("x")
    e1 = Symbol("e1")
    e1_d1x = Symbol("e1_d1x")
    ref_dR = Routine("test1_d1x")
    ref_dR.inputs = [x]
    ref_dR.outputs = [e1, e1_d1x]
    ref_dR.stmts = [Statement(e1, 2 * x ** 2 + 3 * x), Statement(e1_d1x, 4 * x + 3)]
```


The more compact string input:
```
    dtext1 = """
        e0 = 2*x**2 + 3*x
        e0_d1x = 4*x + 3
    """

    ref_dR = routine_from_text("test1_d1x", dtext1)
```


The tests can be run with `pytest`.



