import numpy as np
import os

from create_subdirs import create_subdirs

# every mock should be identifiable via a "mock_file"; I could create an array of absolute mock files and should be able to do everything
#   via that mock_file, and via globals; no internally-defined parameters

def initialize_vals():
    # gradient values
    global grad_dim
    grad_dim = 1        # dimension of w_hat in gradient mock

    global lognormal_density
    lognormal_density = "2e-4"

    global path_to_lognorm_source
    path_to_lognorm_source = f"/scratch/ksf293/mocks/lognormal/cat_L750_n{lognormal_density}_z057_patchy"

    global path_to_data_dir
    path_to_data_dir = f"/scratch/aew492/research-summer2020_output/{grad_dim}D"

    global grad_type
    grad_type = "1rlz_per_m"

    global n_mocks
    n_mocks = 201

    global mocks_info

    global mock_file_name_list
    mock_file_name_list = []

    global mock_name_list
    mock_name_list = []

    global lognorm_file_list
    global m_arr
    global b_arr

    if grad_type == "1rlz":
        m_arr = np.linspace(-1.0, 1.0, n_mocks)
        b_arr = 0.5 * np.ones([n_mocks])
        lognorm_file_list = [f"cat_L750_n{lognormal_density}_z057_patchy_lognormal_rlz1"]
        for m in m_arr:
            for b in b_arr:
                mock_file_name = "{}_m-{:.3f}-L_b-{:.3f}".format(lognorm_file_list[0], m, b)
                mock_file_name_list.append(mock_file_name)
                mock_name = "n{}, m={:.3f}, b={:.3f}".format(lognormal_density, m, b)
                mock_name_list.append(mock_name)

    elif grad_type == "1m":
        m = 0.5
        b = 0.5
        m_arr = m * np.ones([n_mocks])
        b_arr = b * np.ones([n_mocks])
        lognorm_file_list = []
        for i in range(n_mocks):
            lognorm_file_list.append(f"cat_L750_n{lognormal_density}_z057_patchy_lognormal_rlz{i}")

        for lognorm_file in lognorm_file_list:
            mock_file_name = "{}_m-{:.3f}-L_b-{:.3f}".format(lognorm_file, m, b)
            mock_file_name_list.append(mock_file_name)
            mock_name = "n{}, m={:.3f}, b={:.3f}".format(lognormal_density, m, b)
            mock_name_list.append(mock_name)
    
    elif grad_type == "1rlz_per_m":
        b = 0.5
        m_arr = np.linspace(-1.0, 1.0, n_mocks)
        b_arr = b * np.ones([n_mocks])
        lognorm_file_list = []
        for i in range(n_mocks):
            lognorm_file_list.append(f"cat_L750_n{lognormal_density}_z057_patchy_lognormal_rlz{i}")

        # make sure each m value corresponds to its own lognorm rlz
        assert len(m_arr) == len(lognorm_file_list)

        for i in range(len(m_arr)):
            mock_file_name = "{}_m-{:.3f}-L_b-{:.3f}".format(lognorm_file_list[i], m_arr[i], b)
            mock_file_name_list.append(mock_file_name)
            mock_name = "n{}, m={:.3f}, b={:.3f}".format(lognormal_density, m_arr[i], b)
            mock_name_list.append(mock_name)
    
    else:
        print("'grad_type' must be '1rlz', '1m', or '1rlz_per_m'")
        assert False

    # parameters for landy-szalay:
    #   by default in patchify_xi.xi, periodic=False, rmin=20.0, rmax=100.0, nbins=22
    global randmult
    randmult = 2
    global periodic
    periodic = False
    global rmin
    rmin = 20.0
    global rmax
    rmax = 140.0
    global nbins
    nbins = 22
    global nthreads
    nthreads = 12

    # patch values
    global n_patches
    n_patches = 8          # should be n_sides**3

#initialize_vals()