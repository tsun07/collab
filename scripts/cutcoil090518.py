#!/usr/bin/env python

from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys

if len(sys.argv) != 2:
   print "Error! Wrong number of arguments"
   exit(1)

filename = sys.argv[1]
f = netcdf.netcdf_file(sys.argv[1],'r',mmap=False)
ntheta_coil = f.variables['ntheta_coil'][()]
nzeta_coil = f.variables['nzeta_coil'][()]
theta_coil = f.variables['theta_coil'][()]
zeta_coil = f.variables['zeta_coil'][()]
current_potential = f.variables['current_potential'][()]

try:
    nlambda = f.variables['nlambda'][()]
    lambdas = f.variables['lambda'][()]
except:
    nlambda = f.variables['nalpha'][()]
    lambdas = f.variables['alpha'][()]
f.close()

#----functions--------------
def funcEllipse(rshift,rc,zs,polAng,torAng):
    npol = len(polAng)
    ntor = len(torAng)
    polAng,torAng = np.meshgrid(polAng,torAng) #f[tor,pol]
    rr = np.zeros((ntor,npol))
    zz = np.zeros((ntor,npol))
    xx = np.zeros((ntor,npol))
    yy = np.zeros((ntor,npol))
    for i in range(ntor):
        for j in range(npol):
            rr[i,j] = rc*np.cos(polAng[i,j])+rshift
            zz[i,j] = zs*np.sin(polAng[i,j])
            xx[i,j] = rr[i,j]*np.cos(torAng[i,j])
            yy[i,j] = rr[i,j]*np.sin(torAng[i,j])
    return xx,yy,zz,rr
#---------------------------
cdata = plt.contour(zeta_coil,theta_coil,np.transpose(current_potential[2,:,:]))
numCoilsFound = len(cdata.collections)
print(numCoilsFound)
aa = 3.0
bb = 5.0
R0 = 6.0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for j in range(1):#(numCoilsFound):
   p = cdata.collections[j].get_paths()[0]
   v = p.vertices

   contour_zeta = v[:,0]
   contour_theta=v[:,1]

   print('zeta',contour_zeta,'theta',contour_theta)
   x,y,z,R=funcEllipse(R0,aa,bb,contour_theta,contour_zeta)
  	 
   #ax.plot(x[0,:],y[0,:],z[0,:])
   ax.scatter(x[:,:],y[:,:],z[:,:])
   plt.axis('equal')
plt.show()


