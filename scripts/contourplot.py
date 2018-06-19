import numpy as np
import matplotlib.pyplot as plt
import matplotlib

n1 = 101
n2 = 51

x1 = np.linspace(0, 2.*np.pi, n1)
x2 = np.linspace(0, 2.*np.pi, n2)

X1, X2 = np.meshgrid(x1,x2)

Z = np.sin(X1)*np.cos(X2)

breaks = np.linspace(-0.5, 0.5, 2)
print(breaks)
plt.figure()
CS1 = plt.contour(x1, x2, Z,
levels = breaks)
print('coll',CS1.collections)
plt.clabel(CS1,inline=0)
plt.colorbar(ticks=breaks)
plt.show()
