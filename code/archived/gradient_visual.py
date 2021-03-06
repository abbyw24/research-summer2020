import numpy as np
import matplotlib.pyplot as plt

import globals

globals.initialize_vals()  # brings in all the default parameters

grad_dim = globals.grad_dim
L = globals.L
loop = globals.loop
m_arr_perL = globals.m_arr_perL
b_arr = globals.b_arr

periodic = globals.periodic
rmin = globals.rmin
rmax = globals.rmax
nbins = globals.nbins
nthreads = globals.nthreads

n_sides = globals.n_sides

n_patches = n_sides**3

# create plot
fig1 = plt.figure()
plt.xlabel("Expected Gradient")
plt.ylabel("Recovered Gradient")
plt.title("Expected vs. Recovered Gradient")

expected_xgrads = []

def label_s(i):
    if i == 0:
        return "suave"
    else:
        return None

def label_p(i):
    if i == 0:
        return "patches"
    else:
        return None

i = 0

# loop through m and b values
for m in m_arr_perL:
    for b in b_arr:

        # load in data from suave gradient recovery
        suave_data = np.load(f"gradient_mocks/{grad_dim}D/suave/exp_vs_rec_vals/suave_exp_vs_rec_vals_m-{m}-L_b-{b}.npy", allow_pickle=True).item()
        m_s = suave_data["m"]
        b_s = suave_data["b"]
        amps = suave_data["amps"]
        grad_expected_s = suave_data["grad_expected"]
        grad_recovered_s = suave_data["grad_recovered"]
        
        # load in data from patches gradient recovery
        patches_data = np.load(f"gradient_mocks/{grad_dim}D/patches/exp_vs_rec_vals/patches_exp_vs_rec_vals_m-{m}-L_b-{b}_{n_patches}patches.npy", allow_pickle=True).item()
        m_p = patches_data["m"]
        b_p = patches_data["b"]
        n_patches = patches_data["n_patches"]
        grad_expected_p = patches_data["grad_expected"]
        grad_recovered_p = patches_data["grad_recovered"]

        # make sure the data that should match does actually match
        assert m_s == m_p
        m = m_s
        assert b_s == b_p
        b = b_s

        # save expected gradients so we can pull out the max value for plotting
        expected_xgrads.append(grad_expected_s[0])

        # plot expected vs. recovered (in x direction only) for suave
        plt.plot(grad_expected_s[0], grad_recovered_s[0], marker=".", color="C0", alpha=0.5, label=label_s(i))
        # plot expected vs. recovered (in x direction only) for patches
        plt.plot(grad_expected_p[0], grad_recovered_p[0], marker=".", color="orange", alpha=0.5, label=label_p(i))

        # increase index value
        i += 1

# plot line y = x (the data points would fall on this line if the expected and recovered gradients matched up perfectly)
x = np.linspace(min(expected_xgrads), max(expected_xgrads), 10)

plt.plot(x, x, color="black", alpha=0.5)
plt.legend()

plt.show()

fig1.savefig(f"gradient_mocks/{grad_dim}D/exp_vs_rec.png")