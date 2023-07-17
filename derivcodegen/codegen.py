from sympy import Symbol
from sympy.codegen.ast import (
    Assignment,
    Return,
    FunctionDefinition,
    CodeBlock,
    Variable,
    Pointer,
    Declaration,
)
from sympy.printing.julia import JuliaCodePrinter
from sympy.printing.cxx import CXX11CodePrinter
from routine import Routine, Statement

# Node for a C++ reference
class Reference(Pointer):
    """Represents a C++ reference"""

    pass


def convert_stmt_to_assign(stmt):
    if len(stmt.lhs) == 1:
        a = Assignment(Symbol(str(stmt.lhs[0])), stmt.rhs)
    else:
        a =  Assignment(Symbol(str(stmt.lhs)), stmt.rhs)
    return a


# Convert Routine to Sympy codegen AST
def convert_routine_to_function(R, is_cpp=False):
    body = list()

    # For C++, need to declare types for variables
    #  Skip the output variables (except the first one) since those are declared
    #   in the parameter list
    if is_cpp:
        for stmt in R.stmts:
            for lhs_var in stmt.lhs:
                if lhs_var not in R.outputs[1:]:
                    body.append(Variable(str(lhs_var), type="double").as_Declaration())

    # Main loop to convert statements
    for stmt in R.stmts:
        a = convert_stmt_to_assign(stmt)
        body.append(a)

    # For C++, pass all but the first return value as a reference
    if is_cpp:
        body.append(Return(R.outputs[0]))
    else:
        if len(R.outputs) == 1:
            body.append(Return(R.outputs[0]))
        else:
            body.append(Return(tuple(R.outputs)))

    cb = CodeBlock(*body)

    # Input parameters
    input_args = list()
    for inp in R.inputs:
        ivar = Variable(inp, type="double")
        input_args.append(ivar)

    # For C++, pass all but the first return value as a reference
    if is_cpp:
        for out in R.outputs[1:]:
            ovar = Reference(out, type="double")
            input_args.append(ovar)

    func = FunctionDefinition("double", R.name, input_args, cb)

    return func


class AltJuliaCodePrinter(JuliaCodePrinter):
    def __init__(self, settings=None):
        if not settings:
            settings = dict()
        super(AltJuliaCodePrinter, self).__init__(settings=settings)

    def _print_FunctionDefinition(self, expr):
        parms = ", ".join([self._print(e) for e in expr.parameters])
        body = self._print(expr.body)
        return "function {}({})\n{}\nend".format(expr.name, parms, body)

    def _print_Return(self, expr):
        try:
            if len(expr.args[0]) == 1:
                return "return {}".format(self._print(expr.args[0][0]))
            else:
                return "return {}".format(self._print(expr.args[0]))
        except TypeError:
            return "return {}".format(self._print(expr.args[0]))


class AltCXX11CodePrinter(CXX11CodePrinter):
    def __init__(self, settings=None):
        super(AltCXX11CodePrinter, self).__init__(settings=settings)

    def _print_Declaration(self, decl):
        var = decl.variable
        val = var.value
        if isinstance(var, Reference):
            result = "{t}& {s}".format(
                t=self._print(var.type), s=self._print(var.symbol)
            )
            return result
        else:
            return super(AltCXX11CodePrinter, self)._print_Declaration(decl)
