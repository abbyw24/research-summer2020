from patchify_xi import patchify, xi, xi_in_patches

import globals

globals.initialize_vals()  # brings in all the default parameters

grad_dim = globals.grad_dim
L = globals.L
loop = globals.loop
m_arr_perL = globals.m_arr_perL
b_arr = globals.b_arr

randmult = globals.randmult
periodic = globals.periodic
rmin = globals.rmin
rmax = globals.rmax
nbins = globals.nbins
nthreads = globals.nthreads

n_patches = globals.n_patches

lognorm_file = "cat_L750_n2e-4_z057_patchy_lognormal_rlz0" #.bin
path_to_mocks_dir = f"mocks/{grad_dim}D/{lognorm_file}"

# loop through m and b arrays
for m in m_arr_perL:
    for b in b_arr:
        mock_name = "m-{:.2f}-L_b-{:.2f}".format(m, b)
        xi_in_patches(grad_dim, path_to_mocks_dir, mock_name)