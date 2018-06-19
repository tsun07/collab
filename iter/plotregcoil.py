#!/usr/bin/env python
print "usage: regcoilPlot regcoil_out.XXX.nc"

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
import numpy as np
from scipy.io import netcdf
from scipy.interpolate import interp1d
import sys
import math

if len(sys.argv) != 2:
    print "Error! You must specify 1 argument: the regcoil_out.XXX.nc file."
    exit(1)

f = netcdf.netcdf_file(sys.argv[1],'r',mmap=False)
nfp = f.variables['nfp'][()]#?n=1
ntheta_plasma = f.variables['ntheta_plasma'][()]#128
ntheta_coil = f.variables['ntheta_coil'][()]#128
nzeta_plasma = f.variables['nzeta_plasma'][()]
nzeta_coil = f.variables['nzeta_coil'][()]
nzetal_plasma = f.variables['nzetal_plasma'][()]
nzetal_coil = f.variables['nzetal_coil'][()]
theta_plasma = f.variables['theta_plasma'][()]
theta_coil = f.variables['theta_coil'][()]
zeta_plasma = f.variables['zeta_plasma'][()]
zeta_coil = f.variables['zeta_coil'][()]
zetal_plasma = f.variables['zetal_plasma'][()]
zetal_coil = f.variables['zetal_coil'][()]
r_plasma  = f.variables['r_plasma'][()] #?
r_coil  = f.variables['r_coil'][()]
xm_coil = f.variables['xm_coil'][()]
xn_coil = f.variables['xn_coil'][()]
mnmax_coil = f.variables['mnmax_coil'][()]
chi2_B = f.variables['chi2_B'][()]
single_valued_current_potential_thetazeta = f.variables['single_valued_current_potential_thetazeta'][()]
current_potential = f.variables['current_potential'][()]
Bnormal_from_plasma_current = f.variables['Bnormal_from_plasma_current'][()]
Bnormal_from_net_coil_currents = f.variables['Bnormal_from_net_coil_currents'][()]
Bnormal_total = f.variables['Bnormal_total'][()]
net_poloidal_current_Amperes = f.variables['net_poloidal_current_Amperes'][()]

try:
    nlambda = f.variables['nlambda'][()]
    lambdas = f.variables['lambda'][()]
except:
    nlambda = f.variables['nalpha'][()]
    lambdas = f.variables['alpha'][()]

# K used to be called J, so try both names for backward-compatibility.
try:
    chi2_K = f.variables['chi2_K'][()]
    K2 = f.variables['K2'][()]
except:
    chi2_K = f.variables['chi2_J'][()]
    K2 = f.variables['J2'][()]

f.close()



def funcifft2(var_zeta,var_theta,pc,ps,nlen):
	pp = 0.
	for nn in range(1,nlen):
		for mm in range(1,nlen):
			pp = pp + 2.*pc[nn,mm]*np.cos(nn*var_zeta+mm*var_theta)\
				 - 2.* ps[nn,mm]*np.sin(nn*var_zeta+mm*var_theta)
	pp = pp + pc[0,0]
	return pp
'''
xx = r_coil[:,:,0] #[zeta,theta]
yy = r_coil[:,:,1]
zz = r_coil[:,:,2]
xfft = np.fft.fft(xx[:,:])/ntheta_coil  #or /nzeta
yfft = np.fft.fft(yy[:,:])/ntheta_coil
zfft = np.fft.fft(zz[:,:])/ntheta_coil

xfft_r = xfft.real
xfft_i = xfft.imag
x_coil = np.zeros((nzeta_coil,ntheta_coil))
for i in range(nzeta_coil):
	for j in range(ntheta_coil):
		print(i,j)
		x_coil[i,j]= funcifft2(zeta_coil[i],theta_coil[j],xfft_r,xfft_i,ntheta_coil)
if 1:
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot(xx)
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot(x_coil)	
'''
if 0:
	rr = np.sqrt(xx**2+yy**2)
	print('z',max(rr[0,:]),min(rr[0,:]))
	plt.figure()
	plt.plot(rr[0,:],zz[0,:])
	plt.axis('equal')
if 0:
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(xx,yy,zz)
if 1:
	plt.figure()
	plt.contour(zeta_coil,theta_coil,np.transpose(current_potential[9,:,:]))
	plt.colorbar()


plt.show()

