import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ndim = 128
theta = np.linspace(0.,2.*np.pi,num = ndim)
zeta = np.linspace(0.,2.*np.pi, num = ndim)
theta, zeta = np.meshgrid(theta,zeta) #[zeta,theta]
aa = 3.0
bb = 5.0
R0 = 6.0
R = R0 + aa*np.cos(theta)
Z = bb*np.sin(theta)
xx = R*np.cos(zeta)
yy = R*np.sin(zeta)
zz = Z

#----Read plasma boundary---
filepath = "/u/tsun/ITER_RMP/ITER_RMP_n1/"
filename = "gpec.boundary"  #sys.argv[1]
f = open(filepath+filename, "r")
line = f.readline()  #skip
line = f.readline()  #1st line
bmn = int(line.split()[0])
bnfp = int(line.split()[1])
nbf = int(line.split()[2])
line = f.readline() #skip
line = f.readline() #skip
coeff = np.zeros((bmn,6),dtype = np.float64)
for i in range(bmn):
    line = f.readline()  #line5
    #coeff[i,0]= float(int(line.split()[0]))
    coeff[i,1] = float(line.split()[1]) #m
    coeff[i,2] = float(line.split()[2])#rbc ?missing last digit
    coeff[i,3] = float(line.split()[3])#rbs
    coeff[i,4] = float(line.split()[4])#zbc
    coeff[i,5] = float(line.split()[5])#zbs

R_pla = np.zeros(ndim)
Z_pla = np.zeros(ndim)
for j in range(ndim):
	for k in range(bmn):
		R_pla[j] = R_pla[j] + coeff[k,2]*np.cos(coeff[k,1]*theta[0,j]) \
					+ coeff[k,3]*np.sin(coeff[k,1]*theta[0,j])
		Z_pla[j] = Z_pla[j] + coeff[k,4]*np.cos(coeff[k,1]*theta[0,j]) \
					+ coeff[k,5]*np.sin(coeff[k,1]*theta[0,j])
#---------------------------

fig1 = plt.figure()
plt.plot(R_pla,Z_pla,label='Plamsa boundary')
plt.plot(R[0,:],Z[0,:],label='Ellipse winding surface')
plt.legend()
plt.axis('equal')
fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')
ax.plot_surface(xx,yy,zz)
plt.show()
