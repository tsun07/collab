#!/usr/bin/env python

from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
import funcollec

if len(sys.argv) != 3:
   print "Error! Wrong number of arguments:outputFile, surfaceName"
   exit(1)

filename = sys.argv[1]
surfname = sys.argv[2]
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
theta = np.linspace(0.,2.*np.pi,100)
zeta = theta
mtotal, surface_array = funcollec.read_surface(surfname)
xt,yt,rt,zt = funcollec.real_space(mtotal,surface_array,zeta,theta)
lambdas = 2#99
current_potential_plot = current_potential[lambdas,:,:]
ncont = 4
breaks = np.linspace(np.amin(current_potential_plot)-1.,np.amax(current_potential_plot)+1.,ncont)
#breaks = np.linspace(-3001.,3001,ncont)
plt.figure()
cdata = plt.contour(zeta_coil,theta_coil,np.transpose(current_potential_plot),breaks)
plt.clabel(cdata,inline=0)
plt.colorbar(ticks=breaks)

#plt.figure()
contour_zeta = []
contour_theta = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
coilsFilename = 'coils.iter'
f = open(coilsFilename,'w')
f.write('periods '+str(1)+'\n')
f.write('begin filament\n')
f.write('mirror NIL\n')
print('numContour',len(cdata.collections))
for j in range(len(cdata.collections)):
#index_del0 = [0,1,3,4]
#index_del0 = [3] #discon
#for j in index_del0:
	if abs(breaks[j]) >1e-7:
		print('j',j,'Contour Value',breaks[j])
		parts = len(cdata.collections[j].get_paths())
		print('Parts of lines',parts)
		arr = []
		for i in range(parts):
			p = cdata.collections[j].get_paths()[i]
			v = p.vertices

			contour_zeta = v[:,0]
			contour_theta = v[:,1]	
			contour_zeta = np.array(contour_zeta)
			contour_theta = np.array(contour_theta)
			print('end',contour_theta[0],contour_theta[-1],contour_zeta[0],contour_zeta[-1])
			if (abs(contour_theta[0]-contour_theta[-1]) < 1.e-3):	
				#plt.plot(contour_zeta,contour_theta,color='k')

				X,Y,R,Z = funcollec.real_space(mtotal,surface_array,contour_theta,contour_zeta)
				X = np.diagonal(X)
				Y = np.diagonal(Y)
				R = np.diagonal(R)
				Z = np.diagonal(Z)
				#ax.scatter(X,Y,Z)
				ax.plot(X,Y,Z)
				for ii in range(len(X)-1):
					f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e}\n'.format(X[ii],Y[ii],Z[ii],100))
				ii = 0
				f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e} 1 Modular\n'.format(X[ii],Y[ii],Z[ii],0))
				print('coils saved')
			else:
				if i%2 == 0:
					p1 = cdata.collections[j].get_paths()[i]
					v1 = p1.vertices	
					p2 = cdata.collections[j].get_paths()[i+1]
					v2 = p2.vertices
					#print(v1.shape,v2.shape)
					v0 = np.array((1,2))
					v0 = v1[0:1,:]
					#print(v0.shape)
					v = np.concatenate((v1,v2,v0),axis = 0)
					contour_zeta = v[:,0]
					contour_theta = v[:,1]
					contour_zeta = np.array(contour_zeta)
					contour_theta = np.array(contour_theta)
					X,Y,R,Z = funcollec.real_space(mtotal,surface_array,contour_theta,contour_zeta)
					X = np.diagonal(X)
					Y = np.diagonal(Y)
					R = np.diagonal(R)
					Z = np.diagonal(Z)
					#ax.scatter(X,Y,Z)
					ax.plot(X,Y,Z)
					for ii in range(len(X)-1):
						f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e}\n'.format(X[ii],Y[ii],Z[ii],100))
					ii = 0
					f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e} 1 Modular\n'.format(X[ii],Y[ii],Z[ii],0))
				print('dis coils saved')
f.close()

plt.show()
