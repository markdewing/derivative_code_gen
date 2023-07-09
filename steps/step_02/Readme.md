
## Second step - taking the derivative


Now for the initial implementation of the function to take the derivative of the routine.

There are bookkeeping issues with how to name the derivative function and new variables.
The convention here to is to append `d` plus the derivative order and the differentiation variable.
For a function (or variable) named `test` , the derivative function (with respect to `x`) is `test_d1x`.  Multiple variables and orders get concatenated.
For the `test` name with respect to `x` and `y` the derivative name is `test_d1x_d1y`.


The input to the `diff` function is a list of variables and orders.
There are some immediate shortcuts we can implement to make usage a little nicer.
A single variable is converted to a list of size one, and variables without an associated order are assumed to be first derivatives.


These calls should all be equivalent:
```
R.diff(x)
R.diff( [x] )
R.diff( (x, 1) )
R.diff( [(x, 1)] )
```


The input routine in example\_02:
```
Routine: test1
 Inputs:  [x]
 Statements:
   e1  =  2*x**2 + 3*x
 Outputs:  [e1]
```

The derivative routine after calling `R.diff(x)`
```
Routine: test1_d1x
 Inputs:  [x]
 Statements:
   e1  =  2*x**2 + 3*x
   e1_d1x  =  4*x + 3
 Outputs:  [e1, e1_d1x]

```
