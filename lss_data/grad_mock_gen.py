import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import read_lognormal

# pick a seed number so that random set stays the same every time
np.random.seed(123456)

# LOGNORMAL SET
# read in mock data
Lx, Ly, Lz, N, data = read_lognormal.read('/Users/abbywilliams/Physics/research/lss_data/lognormal_mocks/cat_L750_n3e-4_lognormal_rlz0.bin')
    # define boxsize based on mock; and N = number of data points
L = Lx
    # L = boxsize

x_lognorm, y_lognorm, z_lognorm, vx_lognorm, vy_lognorm, vz_lognorm = data.T
xs_clust = x_lognorm, y_lognorm, z_lognorm = np.array([x_lognorm, y_lognorm, z_lognorm])-(L/2)

# DEAD SET
# generate a random data set (same size as mock)
xs_uncl = np.random.uniform(-L/2,L/2,(3,N))

# generate unit vector– this is the direction of the gradient
w_hat = np.random.normal(size=3)
w_hat[2] = 0
    # set z-coordinate to zero for visualisation purposes
w_hat = np.array([0,1,0])
np.linalg.norm(w_hat) == 1
print(w_hat)

# define control parameters m and b
m_arr = np.array([0.0,0.3,1.0,10.0])/L
b_arr = np.array([0.0,0.5,0.75,1.0])

# for each catalog, make random uniform deviates
rs_clust = np.random.uniform(size=N)
rs_uncl = np.random.uniform(size=N)

# dot product onto the unit vectors
ws_clust = np.dot(w_hat,xs_clust)
ws_uncl = np.dot(w_hat,xs_uncl)

# loop through the different m and b parameters
for m in m_arr:
    for b in b_arr:
        # combine catalogs:
        # threshold
        ts_clust = m * ws_clust + b
        ts_uncl = m * ws_uncl + b

        # assert that ts range from 0 to 1
        # assert np.all(ts_clust > 0)
        # assert np.all(ts_clust < 1)

        # desired indices
        I_clust = rs_clust < ts_clust
        I_uncl = rs_uncl > ts_uncl
        # append
        xs = np.append(xs_clust.T[I_clust], xs_uncl.T[I_uncl],axis=0)
        # define this for file name (for saving data and image)
        a = "m-"+str(m*L)+"-L_b-"+str(b)
        # save xs
        np.save("gradient_mocks/grad_mock_"+a,xs)

        # visualisation!
        z_max = -50
        # same color
        xy_slice = xs[np.where(xs[:,2] < z_max)] # select rows where z < z_max

        fig1 = plt.figure()
        plt.plot(xy_slice[:,0],xy_slice[:,1],',')   # plot scatter xy-slice
        plt.plot(xy_slice[:,0],(w_hat[1]/w_hat[0])*xy_slice[:,0],color="green",label=w_hat)   # plot vector w_hat (no z)
        plt.axes().set_aspect("equal")      # square aspect ratio
        plt.ylim((-400,400))
        plt.xlabel("x (Mpc/h)")
        plt.ylabel("y (Mpc/h)")
        plt.title("Gradient Mock, m="+str(m*L)+"/L , b="+str(b))
        plt.legend()
        fig1.savefig("gradient_mocks/grad_mock_"+a+".png")

        # different colors for clust and uncl
        fig2 = plt.figure()

        xs_clust_grad = xs_clust.T[I_clust]
        xs_uncl_grad = xs_uncl.T[I_uncl]

        xy_slice_clust = xs_clust_grad[np.where(xs_clust_grad[:,2] < z_max)]
        xy_slice_uncl = xs_uncl_grad[np.where(xs_uncl_grad[:,2] < z_max)]

        plt.plot(xy_slice_clust[:,0],xy_slice_clust[:,1],',',c="C0",label="clustered")
        plt.plot(xy_slice_uncl[:,0],xy_slice_uncl[:,1],',',c="orange",label="unclustered")
        plt.plot(xy_slice[:,0],(w_hat[1]/w_hat[0])*xy_slice[:,0],c="g",label=w_hat)   # plot vector w_hat (no z)
        plt.axes().set_aspect("equal")      # square aspect ratio
        plt.ylim((-400,400))
        plt.xlabel("x (Mpc/h)")
        plt.ylabel("y (Mpc/h)")
        plt.title("Gradient Mock, m="+str(m*L)+"/L , b="+str(b))
        plt.legend()
        fig2.savefig("gradient_mocks/color_grad_mock_"+a+".png")

        print("m="+str(m)+", b="+str(b)+", done!")