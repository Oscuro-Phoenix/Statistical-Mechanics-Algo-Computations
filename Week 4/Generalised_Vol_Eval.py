import random
import math
import pylab
import numpy as np
import matplotlib.pyplot as plt

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

    
delta = 0.1
n_trials = 500000
Q = 2
d_max = 200
Vol_list = [2]
for d in range(2,d_max+1):
    n_hits = 0
    x = [0] * (d-1)
    old_radius_square = 0
    new_radius_square = 0
    hist = []
    n_hits = 0
    for i in range(n_trials):
        k = random.randint(0, d-2)
        x_old_k = x[k]
        x_new_k = x_old_k + random.uniform(-delta, delta)
        new_radius_square = old_radius_square + x_new_k ** 2 - x_old_k ** 2
        if new_radius_square < 1.0:
            x[k] = x_new_k
            old_radius_square = new_radius_square
        alpha = random.uniform(-1.0, 1.0)
        if old_radius_square + alpha**2 < 1:
            n_hits+=1
            
    Q = Q*2.0*n_hits/float(n_trials)
    Vol_list.append(Q)


dim_arr = np.arange(1,201)
True_vol_list = [V_sph(dim) for dim in dim_arr]
plt.semilogy(dim_arr, Vol_list)
plt.semilogy(dim_arr, True_vol_list)
plt.legend(['Volume','Analytical Volume'])
plt.xlabel('Dimensionality')
plt.ylabel('Volume')
plt.savefig('Volums_vs_Dim.png')
# =============================================================================
# del_r = 0.01
# r = [del_r*N for N in range(0,101)]
# pdf = [20*rad**19 for rad in r]
# plt.hist(hist, bins=100, normed=True)
# plt.plot(r,pdf)
# plt.xlabel('R')
# plt.ylabel('Freq.')
# plt.savefig('Histogram_vs_Smooth_20r^19.png')
# =============================================================================
