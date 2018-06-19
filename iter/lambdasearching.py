from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
import funcollec

if len(sys.argv) != 2:
   print "Error! Wrong number of arguments:outputFile, surfaceName"
   exit(1)

filename = sys.argv[1]
#surfname = sys.argv[2]
f = netcdf.netcdf_file(sys.argv[1],'r',mmap=False)
ntheta_coil = f.variables['ntheta_coil'][()]
nzeta_coil = f.variables['nzeta_coil'][()]
theta_coil = f.variables['theta_coil'][()]
zeta_coil = f.variables['zeta_coil'][()]
current_potential = f.variables['current_potential'][()]
chi2_B = f.variables['chi2_B'][()]
try:
    nlambda = f.variables['nlambda'][()]
    lambdas = f.variables['lambda'][()]
except:
    nlambda = f.variables['nalpha'][()]
    lambdas = f.variables['alpha'][()]

try:
    chi2_K = f.variables['chi2_K'][()]
    K2 = f.variables['K2'][()]
except:
    chi2_K = f.variables['chi2_J'][()]
    K2 = f.variables['J2'][()]
f.close()

plt.plot(chi2_K,chi2_B,'.')
plt.xlabel('chi2_K')
plt.ylabel('chi2_B')
plt.title('lambda searching')
plt.show()
