# Symbolic Derivatives with Code Generation

This project expresses scientific computation in a form that is more like symbolic mathematics.  It performs derivatives on that representation, and then converts to a regular programming language.  It's similar to auto-differentiation, but the diffentiation is done on a different representation.

The representation is a structured collection of statements with the symbolic part using Sympy.

The [steps](steps) directory contains the development progression.   The most complete versions of the code and tests are in the [derivcodegen](derivcodegen) and [tests](tests) directories.


### Example

A function is constructed as
```
    x = Symbol("x")
    e1 = Symbol("e1")
    R = Routine("test1_d1x")
    R.inputs = [x]
    R.outputs = [e1]
    R.stmts = [Statement(e1, 2 * x ** 2 + 3 * x)]
```

or there is a more compact string input, intended for testing

```
    text1 = """
        e0 = 2*x**2 + 3*x
    """

    R = routine_from_text("test1", text1)
```

Take the derivative
```
    x = Symbol('x')
    dR = R.diff(x)
```

Generate the code to a function (Julia in this example.  Python and C++ are also supported targets).
The resulting function is
```
function test1_d1x(x)
    e0 = 2 * x .^ 2 + 3 * x
    e0_d1x = 4 * x + 3
    return (e0, e0_d1x)
end
```

