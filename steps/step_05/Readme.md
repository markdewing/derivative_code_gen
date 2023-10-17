
## Fifth step - more complex derivatives

Now we pick up from the second step, the initial code that took derivatives.
That code works for leaf functions - functions that don't call any other functions (except elementary functions).
For more realistic code, functions will call other functions, and the derivative should handle that.

Functions normally return one value.  When we take the derivative, functions can return more than one value, and that
 no longer works in-line.

Options:

1. Separate functions for each derivative.  This would duplicate a lot of computation in the functions.
2. Add function parameters for derivatives.  This requires modifications to the function (It's a solution used in C++, but passing modifiable parameters can be more difficult in other languages)
3. Move the function call to its own assignment statement.

Option 3 seems the best.  For now we require (assume) that the inputs have this form.
A separate pass to put routines in this form does not seem difficult, but we will leave it for later.


One complication is that functions that compute derivatives return multiple values,
and subsequently the left-hand side of the statement can have multiple variables.
(So far, assigning to a function is the only place this occurs.)
This primary problem comes when applying `diff` multiple times.
To handle this, the Statement type is changed to always use a list on the left side, and the code is adjusted to match.


Naming the function. I had started using the name of the parameter, but that might be
different between the call site and the definition.

Need to pick a standard:
 - Use argument index
 - Use the name from the definition. This requires access to the definition.


For now, use the argument index for simplicity.

Also need to compute which derivatives of which arguments are needed.
This is put in a function to collect the dependencies.
