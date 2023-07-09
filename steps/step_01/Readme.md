
## First step - program representation


We will use a collection of statements, where each statement is an assignment.  The left-hand side is a Sympy variable and the right-hand side is a Sympy expression.
The program representation is held in the class Routine, which consists of a name, a list of statements, a list of input variables, and a list of output variables.

The example routine looks like this printed out:
```
Routine: test1
 Inputs:  [x]
 Statements:
   e1  =  2*x**2
   e2  =  3*e1 + x
 Outputs:  [e2]
```
