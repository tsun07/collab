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
xt,yt,rt,zt = funcollec.real_space_iter3d(mtotal,surface_array,zeta,theta)
n_lambda = 2#38#99
print('lambda',lambdas)
print('mylambda',n_lambda,lambdas[n_lambda])
current_potential_plot = current_potential[n_lambda,:,:]
max_phi = np.amax(current_potential_plot)
max_index=np.where(current_potential_plot==max_phi)
print('max_phi_pos',current_potential_plot[max_index[0],max_index[1]],zeta[max_index[0]],theta[max_index[1]])
ncont = 2
#breaks = np.linspace(0.99*max_phi,max_phi,ncont)
base = 9000
#breaks = [base-1,base,base+1]
breaks = [-base,base]
plt.figure()
cdata = plt.contour(zeta_coil,theta_coil,np.transpose(current_potential_plot),breaks)
plt.clabel(cdata,inline=0)
plt.colorbar(ticks=breaks)
plt.xlabel('zeta')
plt.ylabel('theta')
plt.title('number of coils ='+str(ncont))
#plt.show()
contour_zeta = []
contour_theta = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
numContour = len(cdata.collections)
print(numContour)

plt.show()
