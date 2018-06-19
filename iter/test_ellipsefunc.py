import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

zeta = [1.2,1.5,2.0,1.7,1.4,1.2]
theta =[2.2,2.0,3.0,4.0,3.5,2.2]
t = np.linspace(0.,2.*np.pi,num=100)
#zeta = np.cos(t)
#theta= np.sin(t)
zeta = t
theta = t
aa = 3.0
bb = 5.0
R0 = 6.0
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
x,y,z,R=funcEllipse(R0,aa,bb,theta,zeta)

fig0 = plt.figure()
plt.plot(zeta,theta)
plt.axis('equal')
plt.xlabel('zeta')
plt.ylabel('theta')

fig1 = plt.figure()
plt.plot(R[0,:],z[0,:])
plt.axis('equal')
plt.xlabel('R')
plt.ylabel('Z')

fig2 = plt.figure()
ax = fig2.add_subplot(111,projection='3d')
ax.plot(x[:,0],y[:,0],z[:,0])
plt.axis('equal')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
