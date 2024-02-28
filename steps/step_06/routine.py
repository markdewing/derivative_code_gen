from sympy import (
    diff,
    simplify,
    Symbol,
    Function,
    Derivative,
    Subs,
    IndexedBase,
    Indexed,
)
import sympy.strategies
from sympy.core.function import UndefinedFunction
from collections import OrderedDict

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


# Collect Derivative and Subs expressions.
# This assumes that Subs immediately preceeds a Derivative expression
def collect_Derivative_Subs(expr):
    derivs = set()
    subs = set()

    def find_deriv(e):
        if isinstance(e, Subs):
            subs.add(e)
            return None
        if isinstance(e, Derivative):
            print("e", type(e), e)
            derivs.add(e)
        return e

    sympy.strategies.traverse.top_down(find_deriv)(expr)
    return derivs, subs


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


# Get the argument index for a variable in list of function arguments
def get_argument_index(func_args, var):
    for arg_idx, arg_name in enumerate(func_args):
        if arg_name == var:
            return arg_idx
    return -1


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

        # Check for vectors
        expanded_var_list = expand_var_list_vectors(var_list)
        if self.debug:
            print("Expanded var list = ", expanded_var_list)

        # Name of derivative function
        deriv_routine_name = derivative_routine_name(self.name, var_list, self.inputs)
        dR = Routine(deriv_routine_name)

        # As a starting point, the inputs and outputs are the same as the original function.
        # Assume the new function returns the function value and derivatives.
        dR.inputs = self.inputs[:]
        dR.outputs = self.outputs[:]

        # Collect all the local variables
        local_vars = set()
        for s in self.stmts:
            for lhs in s.lhs:
                local_vars.add(lhs)

        # Collect all the independent variables
        ind_vars = set()
        # for var_sym, order in var_list:
        for var_sym, order in expanded_var_list:
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
            for var_sym, order in expanded_var_list:
                dfunc = Derivative(func, (var_sym, order))
                dvar_name = variable_deriv_name(str(local_var), var_sym, order)
                dfuncs_to_local_vars[dfunc] = Symbol(dvar_name)

        if self.debug:
            print("Local vars to functions: ", local_vars_to_funcs)

        # Keep track of which statments have nonzero derivatives
        deriv_is_nonzero = set()

        # Main loop over statements
        for stmt_idx, s in enumerate(self.stmts):

            # Check for function calls
            # Assume that for all function calls that only the function call in the rhs (e0 = g(x))
            if type(type(s.rhs)) is UndefinedFunction:
                if self.debug:
                    print("Processing function line", str(s))

                # For unknown functions
                dfunc_subs = dict()
                non_zero_dfunc_list = list()
                non_zero_dfunc = dict()

                # for (var, order) in var_list:
                for (var, order) in expanded_var_list:
                    # Convert local variables to functions
                    as_func = s.rhs.subs(local_vars_to_funcs)

                    de_func = diff(as_func, var, order)

                    # dfunc = Derivative(s.rhs, (var, order), evaluate=False)

                    # Convert functions back to local variables
                    de = de_func.subs(dfuncs_to_local_vars).subs(funcs_to_local_vars)

                    de = simplify(de)
                    if de != 0:
                        non_zero_dfunc_list.append((var, order))
                        non_zero_dfunc[(var, order)] = de

                if self.debug:
                    print("nonzero dfunc", non_zero_dfunc)

                args_with_derivs = OrderedDict()

                assign_dict = OrderedDict()  # Use the ordered dict as an OrderedSet
                for lhs_val in s.lhs:
                    assign_dict[lhs_val] = 0

                supporting_dstmts = []
                for var, order in non_zero_dfunc_list:
                    tmp_var3 = variable_deriv_name(str(s.lhs[0]), var, order)

                    # Derivative of UndefinedFunction produces a Derivative if
                    # the argument is a variable.  It produces a Subs(Derivative..
                    # if the argument is an expression involving the variable.

                    de_derivs, de_subs = collect_Derivative_Subs(
                        non_zero_dfunc[(var, order)]
                    )

                    # Create substitutions to convert function Derivatives back
                    # to modified function name calls.
                    for deriv_or_subs in list(de_derivs) + list(de_subs):
                        if isinstance(deriv_or_subs, Subs):
                            deriv = deriv_or_subs.args[0]
                        else:
                            deriv = deriv_or_subs
                        func_args = deriv.args[0].args
                        (var2, order2) = deriv.args[1]
                        arg_idx = get_argument_index(func_args, var2)
                        tmp_var = tmp_variable_name(str(s.lhs[0]), arg_idx, order2)
                        args_with_derivs[(arg_idx, order2)] = 0
                        dfunc_subs[deriv_or_subs] = tmp_var
                        assign_dict[Symbol(tmp_var)] = 0

                    stmt = Statement(
                        Symbol(tmp_var3), non_zero_dfunc[(var, order)].subs(dfunc_subs)
                    )
                    supporting_dstmts.append(stmt)
                    deriv_is_nonzero.add(tmp_var3)

                dfunc_name = derivative_routine_name2(
                    str(type(s.rhs)), args_with_derivs.keys()
                )
                dfunc_call = Function(dfunc_name)(*s.rhs.args)

                assign_list = assign_dict.keys()

                stmt = Statement(tuple(assign_list), dfunc_call)
                dR.stmts.append(stmt)

                dR.stmts.extend(supporting_dstmts)

                # No further processing of this statement
                continue

            # Need the original statement
            dR.stmts.append(s)

            for (var, order) in expanded_var_list:
                if self.debug:
                    print(
                        stmt_idx,
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

                # Remove derivatives known to be zero
                deriv_is_zero = dict()
                for val in dfuncs_to_local_vars.values():
                    if str(val) not in deriv_is_nonzero:
                        deriv_is_zero[val] = 0

                de = de.subs(deriv_is_zero)

                de = simplify(de)
                if de != 0:
                    lhs_deriv_name = variable_deriv_name(str(s.lhs[0]), var, order)

                    if isinstance(var, Indexed):
                        lhs_deriv_name = variable_deriv_name(
                            str(s.lhs[0]), var.base, order
                        )
                        new_lhs = IndexedBase(lhs_deriv_name)[var.indices]
                    else:
                        lhs_deriv_name = variable_deriv_name(str(s.lhs[0]), var, order)
                        new_lhs = Symbol(lhs_deriv_name)

                    deriv_is_nonzero.add(lhs_deriv_name)

                    dstmt = Statement(Symbol(lhs_deriv_name), de)
                    if self.debug:
                        print(stmt_idx, "    derivative: ", dstmt)
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
