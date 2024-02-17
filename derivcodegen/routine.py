from sympy import diff, simplify, Symbol, Function, IndexedBase, Indexed
from sympy.core.function import UndefinedFunction

# Use a class for statements
#  Each has a left-hand side and a right-hand side
class Statement:
    def __init__(self, lhs, rhs):
        if type(lhs) in [list, tuple]:
            self.lhs = list(lhs)
        else:
            self.lhs = [lhs]
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


def expand_var_list_vectors(var_list):
    expanded_var_list = []
    for (var, order) in var_list:
        var_is_vector = isinstance(var, IndexedBase)
        if var_is_vector:
            # Assume vector is of length 3
            for i in range(3):
                expanded_var_list.append((var[i], order))
        else:
            expanded_var_list.append((var, order))

    return expanded_var_list


# Arguments are labeled by index rather than name
def derivative_routine_name(name, var_list, inputs):
    var_name_deriv = name
    for arg_idx, arg in enumerate(inputs):
        for var_name, var_order in var_list:
            if var_name == arg:
                var_name_deriv += f"_d{var_order}arg{arg_idx}"

    return var_name_deriv


# For the called function
def derivative_routine_name2(name, args_with_deriv):
    func_name_deriv = name + "".join(
        "_d" + str(var_order) + "arg" + str(idx) for idx, var_order in args_with_deriv
    )

    return func_name_deriv


def variable_deriv_name(base, var, order):
    return base + "_d" + str(order) + str(var)


def tmp_variable_name(var_name, arg_idx, order):
    return f"tmp_{str(var_name)}_d{str(order)}arg{str(arg_idx)}"


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

    # Does the expr depend on var at statement idx
    def build_dependencies(self, stmts):
        # depends = [set()]*len(stmts)
        depends = list()
        func_dep_map = dict()
        for i in range(len(stmts)):
            depends.append(set())

        for idx, stmt in enumerate(stmts):
            # print('for stmt idx',idx,'free syms',stmt.rhs.free_symbols)
            if type(type(stmt.rhs)) is UndefinedFunction:
                func_args = stmt.rhs.args
                for arg_idx, arg in enumerate(func_args):
                    # print('func arg',arg_idx,arg,arg.free_symbols)
                    func_dep_map[(idx, arg_idx)] = set(arg.free_symbols)
                    for idx2, stmt2 in enumerate(stmts[:idx]):
                        for lhs2 in stmt2.lhs:
                            # print('   checking lhs2',lhs2,' free syms',arg.free_symbols)
                            if lhs2 in arg.free_symbols:
                                # print('   adding ',idx,depends[idx2], ' to ',func_dep_map[(idx,arg_idx)])
                                func_dep_map[(idx, arg_idx)].update(depends[idx2])

            depends[idx].update(stmt.rhs.free_symbols)
            for idx2, stmt2 in enumerate(stmts[:idx]):
                # print('  previous index ',idx2)
                for lhs2 in stmt2.lhs:
                    # print('   checking lhs2',lhs2,' free syms',stmt.rhs.free_symbols)
                    if lhs2 in stmt.rhs.free_symbols:
                        # print('   adding ',idx,depends[idx2], ' to ',depends[idx])
                        depends[idx].update(depends[idx2])

        return depends, func_dep_map

    def print_dependencies(self, stmts, depends, func_dep_map):
        print("Dependency list")
        for idx in range(len(depends)):
            print("stmt ", idx, stmts[idx], " depends on ", depends[idx])
        print("")
        print("Function Dependency list")
        for k, v in func_dep_map.items():
            name = str(stmts[k[0]].rhs)
            print("  ", name, "(stmt idx, arg idx)", k, " depends on", v)
        print("")

    # Takes derivative of a function call
    def diff_function_call(self, idx, s, var_list):
        dR_stmts = []
        func_args = s.rhs.args
        # List of arguments (indices) and the variables
        args_with_deriv = list()
        # List of arguments (indices) and orders with duplicates removed
        args_with_deriv_dict = dict()
        # Find which args have dependencies on which variables
        for arg_idx, arg in enumerate(func_args):
            for var in var_list:
                # print(f'Checking if {var} is in {self.func_dep_map[(idx,arg_idx)]}')
                if var[0] in self.func_dep_map[(idx, arg_idx)]:
                    args_with_deriv_dict[(arg_idx, var[1])] = var
                    args_with_deriv.append((arg_idx, var))

        # Need list of argument indices and orders
        args_with_deriv_list = sorted(args_with_deriv_dict.keys())
        args_and_order = [
            (arg_idx, args_with_deriv_dict[(arg_idx, arg_order)][1])
            for arg_idx, arg_order in args_with_deriv_list
        ]

        if self.debug:
            print("args_with_deriv", args_with_deriv)
            print("args_and_order", args_and_order)

        func_name_deriv = derivative_routine_name2(str(type(s.rhs)), args_and_order)

        assign_list = s.lhs[:]

        tmp_arg_name_list = list()
        for arg_idx, var_order in args_and_order:
            for lhs_var in s.lhs:
                name_var_wrt_var = tmp_variable_name(lhs_var, arg_idx, var_order)
                assign_list.append(Symbol(name_var_wrt_var))
                # tmp_arg_name_list.append(name_var_wrt_var)

        func_call = Function(func_name_deriv)(*s.rhs.args)
        stmt = Statement(tuple(assign_list), func_call)
        if self.debug:
            print(" new function call: ", str(stmt))
        dR_stmts.append(stmt)

        # Now apply the chain rule to the arguments
        # for (arg_idx, (var, order)), tmp_name_var_wrt_var in zip(
        #    args_with_deriv, tmp_arg_name_list
        # ):
        for arg_idx, (var, order) in args_with_deriv:
            for lhs_var in s.lhs:
                name_var_wrt_var = variable_deriv_name(str(lhs_var), var, order)
                tmp_name_var_wrt_var = tmp_variable_name(lhs_var, arg_idx, order)

                expr = 0
                # Loop over function arguments
                for arg in s.rhs.args:
                    if order == 1:
                        darg = diff(arg, var, 1)
                        if self.debug:
                            print(
                                "  Differentiating ",
                                arg,
                                " by ",
                                var,
                                order,
                                " is ",
                                darg,
                            )
                        expr += darg * Symbol(tmp_name_var_wrt_var)

                    if order == 2:
                        tmp_name_var_wrt_var1 = tmp_variable_name(lhs_var, arg_idx, 1)
                        darg1 = diff(arg, var, 1)
                        darg2 = diff(arg, var, 2)
                        if self.debug:
                            print(
                                "  Differentiating ",
                                arg,
                                " by ",
                                var,
                                order,
                                " is ",
                                darg2,
                            )
                        expr += darg1 ** 2 * Symbol(
                            tmp_name_var_wrt_var
                        ) + darg2 * Symbol(tmp_name_var_wrt_var1)

                    for idx2, s2 in enumerate(self.stmts):
                        for lhs_var2 in s2.lhs:
                            if lhs_var2 in arg.free_symbols:
                                name_var_wrt_var2 = variable_deriv_name(
                                    str(lhs_var2), var, order
                                )
                                de2 = diff(arg, lhs_var2, order)
                                expr += (
                                    de2
                                    * Symbol(name_var_wrt_var2)
                                    * Symbol(tmp_name_var_wrt_var)
                                )

                dR_stmts.append(Statement(Symbol(name_var_wrt_var), expr))

        return dR_stmts

    # Compute derivative of function with respect to variables in var_list
    def diff(self, var_list):

        # Allow a single symbol or list of symbols
        if not isinstance(var_list, list):
            var_list = [var_list]

        # Normalize var_list input to be a list of tuples of (Symbol, order)
        var_list = normalize_variable_list(var_list)

        # Check for vectors
        expanded_var_list = expand_var_list_vectors(var_list)
        if self.debug:
            print("Expanded var list = ", expanded_var_list)

        # Name of derivative function
        deriv_routine_name = derivative_routine_name(self.name, var_list, self.inputs)
        dR = Routine(deriv_routine_name)

        self.depends, self.func_dep_map = self.build_dependencies(self.stmts)
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

                func_deriv_stmts = self.diff_function_call(idx, s, var_list)
                dR.stmts.extend(func_deriv_stmts)

                # No further processing of this statement
                continue

            # Need the original statement
            dR.stmts.append(s)

            for (var, order) in expanded_var_list:
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
                    for lhs_var2 in s2.lhs:
                        if lhs_var2 in s.rhs.free_symbols:
                            # Example: y -> y_d1x
                            name_var_wrt_var = variable_deriv_name(
                                str(lhs_var2), var, order
                            )

                            de2 = diff(s.rhs, lhs_var2, order) * Symbol(
                                name_var_wrt_var
                            )
                            de += de2

                de = simplify(de)

                if isinstance(var, Indexed):
                    lhs_deriv_name = variable_deriv_name(str(s.lhs[0]), var.base, order)
                    new_lhs = IndexedBase(lhs_deriv_name)[var.indices]
                else:
                    lhs_deriv_name = variable_deriv_name(str(s.lhs[0]), var, order)
                    new_lhs = Symbol(lhs_deriv_name)

                dstmt = Statement(new_lhs, de)
                if self.debug:
                    print(idx, "    derivative: ", dstmt)
                dR.stmts.append(dstmt)

        # Determine derivatives of output variables
        deriv_outputs = []
        for (var, order) in var_list:
            for outp in self.outputs:
                out_name = variable_deriv_name(str(outp), var, order)
                if isinstance(var, IndexedBase):
                    deriv_outputs.append(IndexedBase(out_name))
                else:
                    deriv_outputs.append(Symbol(out_name))
        dR.outputs.extend(deriv_outputs)

        return dR

    def print(self):
        print("Routine: " + self.name)
        print(" Inputs: ", self.inputs)
        print(" Statements:")
        for s in self.stmts:
            # For the common case where there is only one item on the LHS, skip printing the enclosing brackets
            if len(s.lhs) == 1:
                print("  ", s.lhs[0], " = ", s.rhs)
            else:
                print("  ", s.lhs, " = ", s.rhs)
        print(" Outputs: ", self.outputs)
