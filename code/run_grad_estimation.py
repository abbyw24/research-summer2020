import numpy as np
import os

import read_lognormal
from corrfunc_ls import xi

import globals

globals.initialize_vals()  # brings in all the default parameters

randmult = globals.randmult
periodic = globals.periodic
rmin = globals.rmin
rmax = globals.rmax
nbins = globals.nbins
nthreads = globals.nthreads

mock_2x = read_lognormal.read("/scratch/ksf293/mocks/lognormal/cat_L750_n2e-4_z057_patchy_As2x/cat_L750_n2e-4_z057_patchy_As2x_lognormal_rlz0.bin")
print(type(mock_2x))
print(mock_2x.shape)