
## Step 6 - vectors

So far, all the variables have been assumed to be scalars.
Now we want to expand to vector variables and take component-wise derivatives

In Sympy, array variables have a base type of Indexed (if they have an index), or IndexedBase (if the whole array).

For now, the vector length is assumed to be three.

For the testing utilities, we pass a dictionary of variables to `sympyify`, to
define variables that are not simple scalars.

For now we are going to assume that the inputs and outputs to functions are the
whole array.  The decomposition into components will take place only inside
each function.

For the code generation, one complication is the need to declare storage for
arrays before assigning to components.
For performance, we may eventually want to pass in this storage rather than
allocate it inside the function.  But for now it will be allocated inside
the function.
