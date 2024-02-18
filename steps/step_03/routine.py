from sympy import diff, simplify, Symbol, Function, Derivative

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


def normalize_variable_list(var_list):
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

    return new_var_list


def derivative_routine_name(name, var_list):
    # Note that var[1] is the name of the variable and var[0] is the order
    var_name_deriv = "d" + "_d".join(str(var[1]) + str(var[0]) for var in var_list)
    return name + "_" + var_name_deriv


def variable_deriv_name(base, var, order):
    return base + "_d" + str(order) + str(var)


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

        # Normalize var_list input to be a list of tuples of (Symbol, order)
        var_list = normalize_variable_list(var_list)

        # Name of derivative function
        deriv_routine_name = derivative_routine_name(self.name, var_list)
        dR = Routine(deriv_routine_name)

        # As a starting point, the inputs and outputs are the same as the original function.
        # Assume the new function returns the function value and derivatives.
        dR.inputs = self.inputs[:]
        dR.outputs = self.outputs[:]

        local_vars = set()
        for s in self.stmts:
            local_vars.add(s.lhs)

        # Collect all the independent variables
        ind_vars = set()
        for var_sym, order in var_list:
            ind_vars.add(var_sym)

        # To track dependencies, convert local variables to functions, take the deriviatives,
        # and then convert back.  These are mappings (subs lists) that are needed.

        local_vars_to_funcs = dict()
        funcs_to_local_vars = dict()
        dfuncs_to_local_vars = dict()

        for local_var in local_vars:
            func = Function(local_var)(*ind_vars)
            local_vars_to_funcs[local_var] = func
            funcs_to_local_vars[func] = local_var
            for var_sym, order in var_list:
                dfunc = Derivative(func, (var_sym, order))
                dvar_name = variable_deriv_name(str(local_var), var_sym, order)
                dfuncs_to_local_vars[dfunc] = Symbol(dvar_name)

        if self.debug:
            print("Local vars to functions: ", local_vars_to_funcs)

        # Main loop over statements
        for idx, s in enumerate(self.stmts):
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

                # Convert local variables to functions
                as_func = s.rhs.subs(local_vars_to_funcs)

                # Compute derivative of the statement wrt the variable
                # de = diff(s.rhs, var, order)
                de_func = diff(as_func, var, order)

                # Convert functions back to local variables
                de = de_func.subs(dfuncs_to_local_vars).subs(funcs_to_local_vars)

                de = simplify(de)
                lhs_deriv_name = variable_deriv_name(str(s.lhs), var, order)

                dstmt = Statement(Symbol(lhs_deriv_name), de)
                if self.debug:
                    print(idx, "    derivative: ", dstmt)
                dR.stmts.append(dstmt)

        # Determine derivatives of output variables
        deriv_outputs = []
        for (var, order) in var_list:
            for outp in self.outputs:
                out_name = variable_deriv_name(str(outp), var, order)
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
