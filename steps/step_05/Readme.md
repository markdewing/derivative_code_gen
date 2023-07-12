
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


