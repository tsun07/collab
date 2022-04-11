# -*- coding: utf-8 -*- 
"""
Created on Fri Aug 27 15:43:32 2021

@author: xiangguchn
"""


import time
import json
import numpy as np
import pandas as pd
import scipy.special as sp
import matplotlib.pyplot as plt


# calculate Bv 
def getBfield_PF(rf=0.5, zf=0.0, I_arr=[1,1,1,1,1,1]):
      
    """
      Created on Mon Dec 21 13:10:34 2020    
      @author: tsun
    """
    # st1 = time.time()
    '''Coil parameters'''
    rc = [0.9285,0.9285,2.108,2.108,2.108,2.108]  #coil R centre positions
    zc = [1.913,-1.913,1.335,-1.335,0.445,-0.445] #coil Z centre positions
    hc = [0.215,0.215,0.215,0.215,0.215,0.215]    #height
    wc = [0.143,0.143,0.143,0.143,0.143,0.143]    #width
    Nturn = [22,22,22,22,22,22,22]
    
    
    # st2 = time.time()
    '''Initialisation'''
    mu0 = 2.0e-7  #mu0/2pi
    Br_PF = 0.0
    Bz_PF = 0.0
    
    '''Loop over coils'''
    nc = len(rc)
    # st3 = time.time()
    for i in range(nc):
        
        
        # st4 = time.time()
        rc_min = rc[i] - 0.5*wc[i]
        rc_max = rc[i] + 0.5*wc[i]
        zc_min = zc[i] - 0.5*hc[i]
        zc_max = zc[i] + 0.5*hc[i]
        
        
        # print(zc_min, zc_max)
        
        nr = 2**4
        nz = nr  
        dr = wc[i]/nr
        dz = hc[i]/nz
        
        rcen_1coil = np.linspace(rc_min+0.5*dr,rc_max-0.5*dr,num=nr)
        zcen_1coil = np.linspace(zc_min+0.5*dz,zc_max-0.5*dz,num=nz)
        # print(zcen_1coil)
        
        dI = I_arr[i]*Nturn[i]/(nr*nz)
        for jr in range(nr):
            for jz in range(nz):
                rs = rcen_1coil[jr]
                zs = zcen_1coil[jz]
                
                a = rs
                rho = rf
                z = zf-zs
                
                k2 = 4.0*a*rho/((a+rho)**2+z**2)
                
                E = sp.ellipe(k2)
                K = sp.ellipk(k2)
                
                Br_PF = Br_PF + mu0*dI*z/rho/(((a+rho)**2+z**2)**0.5)*((a**2+rho**2+z**2)/((a-rho)**2+z**2)*E-K)
                Bz_PF = Bz_PF + mu0*dI/(((a+rho)**2+z**2)**0.5)*((a**2-rho**2-z**2)/((a-rho)**2+z**2)*E+K)
                
    return Br_PF, Bz_PF



# Br, Bz = getBfield_PF(rf=0.5, zf=0, I_arr=[1e3, 0, 0, 0, 0, 0])
# print(Bz)
# Br, Bz = getBfield_PF(rf=0.5, zf=0, I_arr=[0, 0, 1e3, 0, 0, 0])
# print(Bz)
# Br, Bz = getBfield_PF(rf=0.5, zf=0, I_arr=[0, 0, 0, 0, 1e3, 0])
# print(Bz)

# rfs, zfs = np.arange(0.2, 0.8, 0.01), np.arange(-0.3, 0.3, 0.01)
rfs, zfs = np.array(r_grid), np.array(z_grid)
nrf, nzf = len(rfs), len(zfs)
Brs, Bzs = np.zeros(shape=(nrf, nzf)), np.zeros(shape=(nrf, nzf))

for i in range(nrf):
    for j in range(nzf):
        print(i,j)
        Br, Bz = getBfield_PF(rf=rfs[i], zf=zfs[j], I_arr=[1e3, 1e3, 1e3, 1e3, 1e3, 1e3])
        Brs[i,j], Bzs[i,j] = Br, Bz

plt.figure(figsize=(10, 10))
X, Y = np.meshgrid(rfs, zfs)
plt.contour(X, Y, Brs, 100)

plt.figure(figsize=(10, 10))
X, Y = np.meshgrid(rfs, zfs)
plt.contour(X, Y, Bzs, 100)

plt.figure(figsize=(10, 10))
X, Y = np.meshgrid(rfs, zfs)
plt.contour(X, Y, np.sqrt(Brs**2+Bzs**2), 200)

scio.savemat('Br_Bz.mat',mdict={'IPFS':[1e3,1e3, 1e3,1e3, 1e3,1e3],'R':X, 'Z':Y, 'Br':Brs, 'Bz':Bzs})







