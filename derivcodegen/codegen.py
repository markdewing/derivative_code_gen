from sympy import Symbol, Indexed, IndexedBase
from sympy.codegen.ast import (
    Assignment,
    Return,
    FunctionDefinition,
    CodeBlock,
    Variable,
    Pointer,
    Declaration,
    Token,
)
from sympy.printing.julia import JuliaCodePrinter
from sympy.printing.pycode import PythonCodePrinter
from sympy.printing.cxx import CXX11CodePrinter
from routine import Routine, Statement

# Node for a C++ reference
class Reference(Pointer):
    """Represents a C++ reference"""

    pass


# Node for array declaration
class ArrayDeclaration(Token):
    __slots__ = ["name", "size"]
    _fields = __slots__


def convert_stmt_to_assign(stmt):
    if len(stmt.lhs) == 1:
        a = Assignment(Symbol(str(stmt.lhs[0])), stmt.rhs)
    else:
        a = Assignment(Symbol(str(stmt.lhs)), stmt.rhs)
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
                    if isinstance(lhs_var, Indexed):
                        pass
                    elif isinstance(lhs_var, IndexedBase):
                        pass
                    else:
                        body.append(
                            Variable(str(lhs_var), type="double").as_Declaration()
                        )

    # Look for arrays that need to be defined
    # For memory efficiency, we may eventually want to pass these as parameters
    array_decls = dict()
    for stmt in R.stmts:
        for lhs_var in stmt.lhs:
            if is_cpp:
                if (
                    isinstance(lhs_var, Indexed)
                    and lhs_var.base not in R.inputs
                    and lhs_var.base not in R.outputs[1:]
                ):
                    array_decls[lhs_var.base] = 3
            else:
                if isinstance(lhs_var, Indexed) and lhs_var.base not in R.inputs:
                    array_decls[lhs_var.base] = 3

    for decl, size in array_decls.items():
        body.append(ArrayDeclaration(decl, size))

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
        if is_cpp and isinstance(inp, IndexedBase):
            ivar = Pointer(inp, type="double")
        else:
            ivar = Variable(inp, type="double")
        input_args.append(ivar)

    # For C++, pass all but the first return value as a reference
    if is_cpp:
        for out in R.outputs[1:]:
            if isinstance(out, IndexedBase):
                ovar = Pointer(out, type="double")
            else:
                ovar = Reference(out, type="double")
            input_args.append(ovar)

    func = FunctionDefinition("double", R.name, input_args, cb)

    return func


class AltJuliaCodePrinter(JuliaCodePrinter):
    def __init__(self, settings=None):
        if not settings:
            settings = dict()
        settings["contract"] = False
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

    # Add 1 to the index to adjust for 1-based array
    def _print_Indexed(self, expr):
        inds = [self._print(i + 1) for i in expr.indices]
        return "%s[%s]" % (self._print(expr.base.label), ",".join(inds))

    def _print_ArrayDeclaration(self, expr):
        return "%s = zeros(%d)" % (expr.name, expr.size)


class AltCXX11CodePrinter(CXX11CodePrinter):
    def __init__(self, settings=None):
        if not settings:
            settings = dict()
        settings["contract"] = False
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

    def _print_ArrayDeclaration(self, expr):
        return "double %s[%d]" % (expr.name, expr.size)

    def _print_Pow(self, expr):
        if expr.exp == 2:
            s = self._print(expr.base)
            return s + "*" + s
        else:
            return super(AltCXX11CodePrinter, self)._print_Pow(expr)


class AltPythonCodePrinter(PythonCodePrinter):
    def __init__(self, settings=None):
        if not settings:
            settings = dict()
        settings["contract"] = False
        super(AltPythonCodePrinter, self).__init__(settings=settings)

    def _print_ArrayDeclaration(self, expr):
        return "%s = np.zeros(%d)" % (expr.name, expr.size)
