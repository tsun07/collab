import numpy as np
import matplotlib.pyplot as plt
import sys
import math

if len(sys.argv) < 1:
    print('Insufficient Arguments')
    print('Requires: file name')
    sys.exit(0)
filepath = "/u/tsun/ITER_RMP/ITER_RMP_n1/"
filename = "gpec.boundary"	#sys.argv[1]
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
	coeff[i,1] = float(line.split()[1])	#m
	coeff[i,2] = float(line.split()[2])#rbc ?missing last digit
	coeff[i,3] = float(line.split()[3])#rbs
	coeff[i,4] = float(line.split()[4])#zbc
	coeff[i,5] = float(line.split()[5])#zbs

ntheta = 100
theta = np.linspace(0.,2.*math.pi,num=ntheta)
R = np.zeros(ntheta)
Z = np.zeros(ntheta)
for j in range(ntheta):
	for k in range(bmn):	
		R[j] = R[j] + coeff[k,2]*math.cos(coeff[k,1]*theta[j]) \
			   + coeff[k,3]*math.sin(coeff[k,1]*theta[j])
		Z[j] = Z[j] + coeff[k,4]*math.cos(coeff[k,1]*theta[j]) \
			   + coeff[k,5]*math.sin(coeff[k,1]*theta[j])
R = R/6.2
Z = Z/6.2
plt.plot(R,Z,label='plasma boundary')
plt.axis('equal')
plt.xlabel('R')
plt.ylabel('Z')
plt.legend()
#plt.show()
