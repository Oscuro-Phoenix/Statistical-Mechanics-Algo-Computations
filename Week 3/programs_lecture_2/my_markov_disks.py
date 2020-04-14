#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:37:14 2020

@author: shakul
"""

import random, math, cmath
import pylab
import matplotlib.pyplot as plt
import os

eta = 0.72 

def delx_dely(x, y):
    d_x = (x[0] - y[0]) % 1.0
    if d_x > 0.5: d_x -= 1.0
    d_y = (x[1] - y[1]) % 1.0
    if d_y > 0.5: d_y -= 1.0
    return d_x, d_y

def Psi_6(L, sigma):
    sum_vector = 0j
    for i in range(N):
        vector  = 0j
        n_neighbor = 0
        for j in range(N):
            if dist(L[i], L[j]) < 2.8 * sigma and i != j:
                n_neighbor += 1
                dx, dy = delx_dely(L[j], L[i])
                angle = cmath.phase(complex(dx, dy))
                vector += cmath.exp(6.0j * angle)
        if n_neighbor > 0:
            vector /= n_neighbor
        sum_vector += vector
    return sum_vector / float(N)

def obtain_config():
    filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)
    if os.path.isfile(filename):
        f = open(filename, 'r')
        L = []
        for line in f:
            a, b = line.split()
            L.append([float(a), float(b)])
        f.close()
        print('starting from file', filename)
    else:
        f = open(filename, 'w')
        L = [[delxy + i * two_delxy, delxy + j * two_delxy] for i in range(N_sqrt) for j in range(N_sqrt)]
        for a in L:
           f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
        f.close()
    return L

def show_conf(L, sigma, title, fname):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  math.sqrt(d_x**2 + d_y**2)
psi = []
for run in range(250000):
    N=64
    if run % 10000 == 0:
        eta = eta - 0.02
    sigma = math.sqrt(eta/(N*math.pi))
    N_sqrt = int(math.sqrt(N))
    delxy = 1/(2*N_sqrt)
    two_delxy = 2*delxy
    sigma_sq = sigma ** 2
    delta = 0.3*sigma
    
    n_steps = 10
    
    if run == 0 or run % 10000 == 0:
     L = obtain_config()
    
     
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        min_dist = min([dist(b,c) for c in L if c != a])
        if not (min_dist < 2.0 * sigma):
            b = [xi % 1.0 for xi in b]
            L[L.index(a)] = b
    #print(L)
    
    if run % 100 == 0:
        psi.append(abs(Psi_6(L,sigma)))
    #show_conf(L, sigma, 'test graph', 'square_N=64.png')

plt.plot(psi)
plt.ylabel('Abs. Psi')
plt.xlabel('# of runs/100')
plt.savefig('Psi_Plot')