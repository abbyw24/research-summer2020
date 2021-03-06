import numpy as np
import matplotlib.pyplot as plt
import os

import globals
from create_subdirs import create_subdirs

globals.initialize_vals()  # brings in all the default parameters

grad_dim = globals.grad_dim
path_to_data_dir = globals.path_to_data_dir
mock_file_name_list = globals.mock_file_name_list
n_mocks = globals.n_mocks

grad_type = globals.grad_type

lognormal_density = globals.lognormal_density

def histogram_patches(n_patches_list, grad_type=grad_type, lognormal_density=lognormal_density, path_to_data_dir=path_to_data_dir, nbins=20):
    # make sure inputs have correct form
    assert isinstance(n_patches_list, list)

    # create the needed subdirectories
    sub_dirs = [
        f"plots/n_patches/histogram/{grad_type}/{n_mocks}mocks"
    ]
    create_subdirs(path_to_data_dir, sub_dirs)
    
    dim = {
            0 : "x",
            1 : "y",
            2 : "z"
            }

    # get recovered and expected gradients
    grads_rec = {}
    grads_exp = {}
    all_grads = []       # to combine grads_rec from all patches; for bin edges

    for n_patches in n_patches_list:
        grads_exp[str(n_patches)] = []
        grads_rec[str(n_patches)] = []
        for i in range(len(mock_file_name_list)):
            mock_info = np.load(os.path.join(path_to_data_dir, f"mock_data/{lognormal_density}/{mock_file_name_list[i]}.npy"), allow_pickle=True).item()
            grad_exp = mock_info["grad_expected"]
            grads_exp[str(n_patches)].append(grad_exp)

            patch_info = np.load(os.path.join(path_to_data_dir, f"patch_data/{lognormal_density}/{n_patches}patches/{mock_file_name_list[i]}.npy"), allow_pickle=True).item()
            grad_rec = patch_info["grad_recovered"]
            grads_rec[str(n_patches)].append(grad_rec)

            all_grads.append(grad_rec-grad_exp)
    
    all_grads = np.array(all_grads)

    # loop through desired dimensions
    for i in dim:
        print(f"{dim[i]}:")
        # create plot
        fig = plt.figure()
        plt.title(f"Histogram of Recovered Grad., {dim[i]}, {grad_type}, {n_mocks} mocks")
        plt.xlabel("Recovered Grad. - Expected Grad.")
        plt.ylabel("Counts")

        # define bins
        bins = np.linspace(1.5*min(all_grads[:,i]), 1.5*max(all_grads[:,i]), nbins)

        a = 0.8
        bin_vals = []
        for n_patches in n_patches_list:
            grads_rec_n = np.array(grads_rec[str(n_patches)])
            grads_exp_n = np.array(grads_exp[str(n_patches)])
            vals = grads_rec_n[:,i] - grads_exp_n[:,i]
            n, _, _ = plt.hist(vals, bins=bins, histtype="step", color="indigo", alpha=a, label=f"{n_patches} patches")
            a /= 2.5
            bin_vals.append(n)
            print(f"for {n_patches} patches:")
            print("mean = ", np.mean(grads_rec_n[:,i]))
            print("min = ", np.min(grads_rec_n[:,i]))
            print("max = ", np.max(grads_rec_n[:,i]))
            print("std = ", np.std(grads_rec_n[:,i]))

        bin_vals = np.array(bin_vals)

        # line at x = 0
        plt.vlines(0, 0, np.amax(bin_vals), color="black", alpha=1, zorder=100, linewidth=1)

        plt.legend()

        fig.savefig(os.path.join(path_to_data_dir, f"plots/n_patches/histogram/{grad_type}/{n_mocks}mocks/hist_n_patches_{nbins}bins_{dim[i]}.png"))
        plt.cla()

        print(f"histogram for n_patches, dim {dim[i]}, done")