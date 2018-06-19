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
mtotal, surface_array = funcollec.read_surface_iter(surfname)
xt,yt,rt,zt = funcollec.real_space_iter3d(mtotal,surface_array,zeta,theta)
n_lambda = 2#38#99
print('lambda',lambdas)
print('mylambda',n_lambda,lambdas[n_lambda])
current_potential_plot = current_potential[n_lambda,:,:]
ncont = 2
base = 9000
breaks = [-base,base]
plt.figure()
cdata = plt.contour(zeta_coil,theta_coil,np.transpose(current_potential_plot),breaks)
plt.clabel(cdata,inline=0)
plt.colorbar(ticks=breaks)
plt.xlabel('zeta')
plt.ylabel('theta')
plt.title('number of coils ='+str(ncont))
#plt.show()
#save to file

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
coilsFilename = 'coils.iter'
f = open(coilsFilename,'w')
f.write('periods '+str(1)+'\n')
f.write('begin filament\n')
f.write('mirror NIL\n')
j = 1
parts = len(cdata.collections[j].get_paths())
for i in range(parts):
	p = cdata.collections[j].get_paths()[i]
	v = p.vertices
	#contour_zeta = v[:,0]
	X,Y,R,Z = funcollec.real_space_iter2d(mtotal,surface_array,v[:,1],v[:,0])	
	ax.plot(X,Y,Z)
	for ii in range(len(X)-1):			
		f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e}\n'.format(X[ii],Y[ii],Z[ii],100))
	ii = 0
	f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e} 1 Modular\n'.format(X[ii],Y[ii],Z[ii],0))
	print('coils saved')
	#shift pi in zeta
	X,Y,R,Z = funcollec.real_space_iter2d(mtotal,surface_array,v[:,1],v[:,0]+np.pi)
	ax.plot(X,Y,Z)
	for ii in range(len(X)-1):
		f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e}\n'.format(X[ii],Y[ii],Z[ii],100))
	ii = 0
	f.write('{:14.22e} {:14.22e} {:14.22e} {:14.22e} 1 Modular\n'.format(X[ii],Y[ii],Z[ii],0))
	print('dis coils saved')
			
			

plt.show()
