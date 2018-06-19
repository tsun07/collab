from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

if len(sys.argv) != 2:
   print "Error! Wrong number of arguments"
   exit(1)

filename = sys.argv[1] #output file

f = netcdf.netcdf_file(filename,'r',mmap=False)
theta = f.variables['theta_coil'][()]
zeta = f.variables['zeta_coil'][()]
nfp = f.variables['nfp'][()] #number of filed periodicity??
net_poloidal_current_Amperes = f.variables['net_poloidal_current_Amperes'][()]#??
current_potential = f.variables['current_potential'][()]
f.close()

plt.figure()
plt.contour(zeta,theta,np.transpose(current_potential[9,:,:]),10)
plt.show()
