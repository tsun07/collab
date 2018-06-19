import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import func	
from matplotlib import cm, colors

fina = '/u/tsun/ITER_RMP/ITER_RMP_n1/gpec.boundary'
zeta = np.linspace(0.,2.*np.pi,100)
theta = zeta
x,y,r,z,b = func.plabry_and_bn_3d(fina,theta,zeta)
strength = b
norm = colors.Normalize(vmin = np.min(strength),vmax = np.max(strength), clip = False)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x,y,z,colors=cm.coolwarm(norm(strength)),cmap=cm.coolwarm)
#cmap=cm.coolwarm,facecolors=cm.coolwarm(norm(strength)))
plt.figure()
plt.plot(b[0,:])
plt.show()



