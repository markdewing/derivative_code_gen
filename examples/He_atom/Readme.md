

# Helium atom

One driving example is the wavefunction for the ground state of a Helium atom.

A description the physics is in this
(Jupyter notebook)[https://github.com/QMCPACK/qmc_algorithms/blob/master/Variational/Variational_Helium.ipynb].

Some more discussion on the integration part of the problem:
(Use of the integrand)[https://markdewing.github.io/blog/posts/integration-callbacks/].

The variational principle states that for any wavefunction, the resulting energy is greater
than or equal to the true ground state energy.
This immediately suggests a method where we guess a parameterized wavefunction, compute the
 energy, and minimize the energy with respect to that parameter.

For the energy, we need the second derivative (Laplacian) with respect to the spatial
positions.  To optimize the energy, we additionally need the derivative with respect to
the variable parameters.


The file `ref_psi.py` has a reference implementation of the wavefunction in Python.

