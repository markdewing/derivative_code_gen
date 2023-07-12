from sympy import diff, simplify, Symbol, Function
from sympy.core.function import UndefinedFunction

# Use a class for statements
#  Each has a left-hand side and a right-hand side
class Statement:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        same = self.lhs == other.lhs and self.rhs == other.rhs
        if not same:
            print("  compare lhs", type(self.lhs), type(other.lhs))
            print("  compare rhs", type(self.rhs), type(other.rhs))
        return same

    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)


class Routine:
    def __init__(self, name):
        self.name = name
        # List of Sympy variables
        self.inputs = []
        # List of Statement objects
        self.stmts = []
        # List of Sympy variables
        self.outputs = []

        self.debug = False

    # Compute derivative of function with respect to variables in var_list
    def diff(self, var_list):

        # Allow a single symbol or list of symbols
        if not isinstance(var_list, list):
            var_list = [var_list]

        # Each variable is a Symbol or tuple of (Symbol, order)
        # Convert so all variable entries are tuples
        new_var_list = []
        for v in var_list:
            if isinstance(v, tuple):
                new_var_list.append(v)
            else:
                new_var_list.append((v, 1))
        var_list = new_var_list
        print("new var list", var_list)

        # Name of derivative function
        # Note that var[1] is the name of the variable and var[0] is the order
        var_name_deriv = "d" + "_d".join(str(var[1]) + str(var[0]) for var in var_list)
        dR = Routine(self.name + "_" + var_name_deriv)

        # As a starting point, the inputs and outputs are the same as the original function.
        # Assume the new function returns the function value and derivatives.
        dR.inputs = self.inputs[:]
        dR.outputs = self.outputs[:]

        # Main loop over statements
        for idx, s in enumerate(self.stmts):

            # Check for function calls
            # Assume that all function calls only the function call in the rhs (e0 = g(x))
            if type(type(s.rhs)) is UndefinedFunction:
                if self.debug:
                    print("Processing function line", str(s))

                func_name_deriv = str(type(s.rhs)) + "".join(
                    "_d" + str(var[1]) + str(var[0]) for var in var_list
                )

                assign_list = [s.lhs]
                for (var, order) in var_list:
                    name_var_wrt_var = (
                        "tmp_" + str(s.lhs) + "_d" + str(order) + str(var)
                    )
                    assign_list.append(Symbol(name_var_wrt_var))

                func_call = Function(func_name_deriv)(*s.rhs.args)
                stmt = Statement(tuple(assign_list), func_call)
                if self.debug:
                    print(" new function call: ", str(stmt))
                dR.stmts.append(stmt)

                tmp_name_var_wrt_var = (
                    "tmp_" + str(s.lhs) + "_d" + str(order) + str(var)
                )
                name_var_wrt_var = str(s.lhs) + "_d" + str(order) + str(var)

                dR.stmts.append(
                    Statement(Symbol(name_var_wrt_var), Symbol(tmp_name_var_wrt_var))
                )

                # No further processing of this statement
                continue

            # Need the original statement
            dR.stmts.append(s)

            for (var, order) in var_list:
                if self.debug:
                    print(
                        idx,
                        "processing stmt ",
                        str(s.lhs),
                        "=",
                        str(s.rhs),
                        " wrt ",
                        var,
                        " free symbols: ",
                        s.rhs.free_symbols,
                    )

                # Compute derivative of the statement wrt the variable
                de = diff(s.rhs, var, order)

                # Derivatives wrt other statements (chain rule)
                for idx2, s2 in enumerate(self.stmts):
                    if s2.lhs in s.rhs.free_symbols:
                        # Example: y -> y_d1x
                        name_var_wrt_var = str(s2.lhs) + "_d" + str(order) + str(var)
                        de2 = diff(s.rhs, s2.lhs, order) * Symbol(name_var_wrt_var)
                        de += de2

                de = simplify(de)
                lhs_deriv_name = str(s.lhs) + "_d" + str(order) + str(var)

                dstmt = Statement(Symbol(lhs_deriv_name), de)
                if self.debug:
                    print(idx, "    derivative: ", dstmt)
                dR.stmts.append(dstmt)

        # Determine derivatives of output variables
        deriv_outputs = []
        for (var, order) in var_list:
            for outp in self.outputs:
                out_name = str(outp) + "_d" + str(order) + str(var)
                deriv_outputs.append(Symbol(out_name))
        dR.outputs.extend(deriv_outputs)

        return dR

    def print(self):
        print("Routine: " + self.name)
        print(" Inputs: ", self.inputs)
        print(" Statements:")
        for s in self.stmts:
            print("  ", s.lhs, " = ", s.rhs)
        print(" Outputs: ", self.outputs)
