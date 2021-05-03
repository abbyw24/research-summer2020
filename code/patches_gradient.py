import numpy as np
import matplotlib.pyplot as plt
import globals

globals.initialize_vals()  # brings in all the default parameters

grad_dim = globals.grad_dim
L = globals.L
m_arr_perL = globals.m_arr_perL
b_arr = globals.b_arr

n_sides = globals.n_sides
n_patches = n_sides**3

# ** this is currently for the x dimension only **

# loop through m and b values
for m in m_arr_perL:
    for b in b_arr:
        print(f"m={m}, b={b} :")

        # load in recovered gradient
        recovered_vals = np.load(f"gradient_mocks/{grad_dim}D/patches/lst_sq_fit/recovered_vals_m-{m}-L_b-{b}_{n_patches}patches.npy")
        m_fit_x, m_fit_y, m_fit_z, b_fit = recovered_vals
        grad_recovered = (1/b_fit)*np.array([m_fit_x,m_fit_y,m_fit_z])
        print("recovered gradient (m_fit/b_fit) =", grad_recovered)

        # expected gradient (only in x direction)
        grad_expected = np.array([m/(b*L),0,0])
        print("expected gradient (m_input/b_input)w_hat =", grad_expected)

        # mean squared error just to see for now how close we are
        mean_sq_err = (1/len(grad_expected))*np.sum((grad_recovered - grad_expected)**2)
        print(f"mean squared error = {mean_sq_err}")

        # projection of recovered onto expected
        grad_exp_norm = np.linalg.norm(grad_expected)
        proj_rec_onto_exp = (np.dot(grad_recovered,grad_expected)/grad_exp_norm**2)*grad_expected

        # residual
        residual = grad_recovered - grad_expected

        # load in mock data
        xs_clust_grad = np.load("gradient_mocks/"+str(grad_dim)+"D/mocks_colored/clust_m-"+str(m)+"-L_b-"+str(b)+".npy")
        xs_uncl_grad = np.load("gradient_mocks/"+str(grad_dim)+"D/mocks_colored/unclust_m-"+str(m)+"-L_b-"+str(b)+".npy")

        z_max = 100

        xy_slice_clust = xs_clust_grad[np.where(xs_clust_grad[:,2] < z_max)]
        xy_slice_uncl = xs_uncl_grad[np.where(xs_uncl_grad[:,2] < z_max)]

        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        plt.plot(xy_slice_clust[:,0],xy_slice_clust[:,1],',',c="C0")
        plt.plot(xy_slice_uncl[:,0],xy_slice_uncl[:,1],',',c="orange")

        # plot expected, recovered, and projection from origin (only in xy)
        V = np.array([grad_expected, grad_recovered, proj_rec_onto_exp])
        colors = np.array(["red", "black", "blue"])
        labels = np.array([r"Expected", r"Recovered", r"Proj. of $\vec{r}$ onto $\vec{e}$"])
        plot_array = np.column_stack((V, colors, labels))
        a = 200*L     # scale factor

        for i in range(len(V)-1):
            plt.plot([0,a*V[i,0]], [0,a*V[i,1]], label=plot_array[i,4], color=plot_array[i,3], alpha=0.8, linewidth=2)
        # plot residual as triangle
        plt.plot([a*grad_expected[0],a*grad_recovered[0]], [a*grad_expected[1],a*residual[1]], color="black", alpha=0.6, label="Residual", linewidth=2)

        plt.title("Expected vs. Recovered Clustering Gradient: \n m="+str(m)+", b="+str(b)+", "+str(n_patches)+" patches")
        plt.ylim((-400,400))
        plt.xlim((-400,400))
        ax.set_aspect("equal")      # square aspect ratio
        plt.xlabel("x (Mpc/h)")
        plt.ylabel("y (Mpc/h)")
        plt.legend()

        fig1.savefig("gradient_mocks/"+str(grad_dim)+"D/patches/lst_sq_fit/grad_exp_vs_rec_m-"+str(m)+"-L_b-"+str(b)+"_"+str(n_patches)+"patches.png")

        # save recovered and expected values to dictionary
        exp_vs_rec_vals = {
            "m" : m,
            "b" : b,
            "n_patches" : n_patches,
            "grad_expected" : grad_expected,
            "grad_recovered" : grad_recovered,
            "mean_sq_err" : mean_sq_err
        }

        np.save(f"gradient_mocks/{grad_dim}D/patches/exp_vs_rec_vals/patches_exp_vs_rec_vals_m-{m}-L_b-{b}_{n_patches}patches", exp_vs_rec_vals)

        print(" ")      # line break for nice loop print formatting