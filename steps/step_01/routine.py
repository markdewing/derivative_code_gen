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
        # List of Statement
        self.stmts = []
        # List of Sympy variables
        self.outputs = []

    def print(self):
        print("Routine: " + self.name)
        print(" Inputs: ", self.inputs)
        print(" Statements:")
        for s in self.stmts:
            print("  ", s.lhs, " = ", s.rhs)
        print(" Outputs: ", self.outputs)
