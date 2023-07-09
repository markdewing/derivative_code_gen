
## Fourth step - code generation

The initial target languages are Python, Julia, and C++.

The Routine is converted to Sympy's AST, which is then output using a code printer.

The code printers don't always have the functionality needed, but it is straightforward to extend them.

For now, all the variables are scalars and have type double.


C++ presents some complications for multiple return values.  The current code adds outputs to the function parameters as references.
In the future, using a tuple type might be better, and require fewer special cases in the code.


The routine
```
  e0 = 2*x
  e1 = exp(-x)
```

Results in the output function in various languages:

Python
```
def test1(x):
    e0 = 2*x
    e1 = math.exp(-x)
    return (e0, e1)
```

Julia
```  
function test1(x)
    e0 = 2 * x
    e1 = exp(-x)
    return (e0, e1)
end
```

C++
```
double test1(double x, double& e1){
   double e0;
   e0 = 2*x;
   e1 = std::exp(-x);
   return e0;
}
```




