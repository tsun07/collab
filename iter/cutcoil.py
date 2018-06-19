#!/usr/bin/env python

from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
import funcollec

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

current_potential_plot = current_potential[2,:,:]
ncont = 5
breaks = np.linspace(np.amin(current_potential_plot),np.amax(current_potential_plot),ncont)
plt.figure()
cdata = plt.contour(zeta_coil,theta_coil,np.transpose(current_potential_plot),breaks)
plt.clabel(cdata,inline=0)
plt.colorbar(ticks=breaks)

#plt.figure()
j = 3
print(breaks[j])
contour_zeta = []
contour_theta = []
#for i in range(len(cdata.collections[j].get_paths())):
i = 2

p = cdata.collections[j].get_paths()[i]
v = p.vertices

contour_zeta = v[:,0]
contour_theta = v[:,1]	
print(contour_zeta.shape)
plt.plot(contour_zeta,contour_theta,color='k')

contour_zeta = np.array(contour_zeta)
contour_theta = np.array(contour_theta)

mtotal, surface_array = funcollec.read_surface('/u/tsun/scripts/iterWinding.txt')
X,Y,R,Z = funcollec.real_space(mtotal,surface_array,contour_theta,contour_zeta)
theta = np.linspace(0.,2.*np.pi,100)
zeta = theta
xt,yt,rt,zt = funcollec.real_space(mtotal,surface_array,theta,zeta)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for ii in range(len(X[:,0])):
	ax.scatter(X[ii,ii],Y[ii,ii],Z[ii,ii])


plt.figure()
plt.plot(rt[0,:],zt[0,:])
plt.plot(R[0,:],Z[0,:])
plt.show()

foa = open('angle.txt','w')
foa.write('zeta,theta\n')
for jj in range(len(contour_zeta)):
	foa.write('{:23.15E}{:23.15E} \n'.format(contour_zeta[jj],contour_theta[jj]))

foa.close()	

coilsFilename = 'coils.iter'
f = open(coilsFilename,'w')
f.write('periods '+str(1)+'\n')
f.write('begin filament\n')
f.write('mirror NIL\n')
numCoils =1
for j in range(numCoils):
   N = len(X[:,0])
   for ii in range(N):
      f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e}\n'.format(X[ii,ii],Y[ii,ii],Z[ii,ii],100))
   # Close the loop
   ii=0
   f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e} 1 Modular\n'.format(X[ii,ii],Y[ii,ii],Z[ii,ii],0))

f.close()
