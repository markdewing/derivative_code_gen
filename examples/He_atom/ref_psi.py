

import numpy as np

# Compute the magnitude of a vector
def mag(r):
    return np.sqrt(r[0]*r[0] + r[1]*r[1] + r[2]*r[2])

# Orbital that localized the electron around the nucleus
def orb(R):
    r = mag(R)
    Z = 2.0
    y = np.exp(-Z*r)
    return y


# The Jastrow factor accounts for interaction (repulsion) between electrons.
# The value "B" is the single adjustable parameter ("variational parameter") in
#  this wavefunction.
def jastrow(r12, B):
    A = 0.5
    return np.exp(A*r12/(1 + B*r12))

# The overall wavefunction for two electrons.
def psi(r1, r2, B):
    o1 = orb(r1)
    o2 = orb(r2)
    r12 = r2 - r1
    r12_mag = mag(r12)
    j = jastrow(r12_mag, B)
    return o1*o2*j


if __name__ == "__main__":
    r1 = np.array([1.0, 2.0, 1.5])
    r2 = np.array([-1.0, 1.0, 1.2])
    B = 0.1

    p = psi(r1, r2, B)
    print("psi = ",p)
