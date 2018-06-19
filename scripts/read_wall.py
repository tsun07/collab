import numpy as np
import matplotlib.pyplot as plt

wallfile = "/u/tsun/ITER_RMP/iter_wall.txt"
f = open(wallfile, "r")
#----R_wall----
line = f.readline()
line = f.readline()
line = f.readline()
#str0 = line.split()[0]
#str1 = line.split()[1]
str2 = line.split()[2]
startnum = int(str2.split('*')[0])
R_wall_start = float(str2.split('*')[1])

R_wall = []
for i in range(startnum):
	R_wall.append(R_wall_start)
R_wall.append(float(line.split()[3]))
R_wall.append(float(line.split()[4]))
R_wall.append(float(line.split()[5]))

for i in range (42):
	line = f.readline()
	R_wall.append(float(line.split()[0]))
	R_wall.append(float(line.split()[1]))
	R_wall.append(float(line.split()[2]))
	R_wall.append(float(line.split()[3]))
	R_wall.append(float(line.split()[4]))

line = f.readline()
str5 = line.split()[0]
endnum = int(str5.split('*')[0])
R_wall_end  = float(str5.split('*')[1])
for i in range (endnum):
	R_wall.append(R_wall_end)
#print(R_wall)
#------END R_wall----

#----Z_wall----
Z_wall = []
for i in range (69):
	line = f.readline()
	nele = len(line.split())
	if nele == 6:
		Z_wall.append(float(line.split()[2]))
		Z_wall.append(float(line.split()[3]))
		Z_wall.append(float(line.split()[4]))
		Z_wall.append(float(line.split()[5]))
	elif nele == 5:
		Z_wall.append(float(line.split()[0]))
		Z_wall.append(float(line.split()[1]))
		Z_wall.append(float(line.split()[2]))
		Z_wall.append(float(line.split()[3]))
		Z_wall.append(float(line.split()[4]))
	elif nele == 4:
		Z_wall.append(float(line.split()[0]))
		Z_wall.append(float(line.split()[1]))
		Z_wall.append(float(line.split()[2]))
		Z_wall.append(float(line.split()[3]))
	elif nele == 1:
		Z_wall.append(float(line.split()[0]))
	else:
		print('Errors from loading')
#----END Z_wall----
line = f.readline()
line = f.readline()
line = f.readline()
line = f.readline()
#----SHELL----
R_shell = []
for i in range (44):
	line = f.readline()
	nele = len(line.split())
	if nele == 6:
		str2 = line.split()[2]
		startnum = int(str2.split('*')[0])
		R_shell_start = float(str2.split('*')[1]) 
		for j in range(startnum):
			R_shell.append(R_shell_start)
		R_shell.append(float(line.split()[3]))
		R_shell.append(float(line.split()[4]))
		R_shell.append(float(line.split()[5]))
	elif nele ==5:
		R_shell.append(float(line.split()[0]))
		R_shell.append(float(line.split()[1]))
		R_shell.append(float(line.split()[2]))
		R_shell.append(float(line.split()[3]))
		R_shell.append(float(line.split()[4]))
	elif nele == 3:
		R_shell.append(float(line.split()[0]))
		R_shell.append(float(line.split()[1]))
		str2 = line.split()[2]
		endnum = int(str2.split('*')[0])
		R_shell_end = float(str2.split('*')[1])
		for j in range(endnum):
			R_shell.append(R_shell_end)
	else:
		print('Errors from loading Rshell')

Z_shell = []
for i in range (68):
	line = f.readline()
	nele = len(line.split())
	if nele == 6:
		Z_shell.append(float(line.split()[2]))
		Z_shell.append(float(line.split()[3]))
		Z_shell.append(float(line.split()[4]))
		Z_shell.append(float(line.split()[5]))
	elif nele == 5:
		Z_shell.append(float(line.split()[0]))
		Z_shell.append(float(line.split()[1]))
		Z_shell.append(float(line.split()[2]))
		Z_shell.append(float(line.split()[3]))
		Z_shell.append(float(line.split()[4]))
	elif nele == 4:
		Z_shell.append(float(line.split()[0]))
		Z_shell.append(float(line.split()[1]))
		Z_shell.append(float(line.split()[2]))
		Z_shell.append(float(line.split()[3]))
	else:
		print('Errors from loading Zshell')
#----END SHELL----
f.close()

plt.plot(R_wall,Z_wall,label='Wall')
plt.plot(R_shell,Z_shell,label='Shell')
plt.axis('equal')
plt.legend()
#plt.show()

R_shell = 6.2*np.array(R_shell)
Z_shell = 6.2*np.array(Z_shell)
R_wall = 6.2*np.array(R_wall)
Z_wall = 6.2*np.array(Z_wall)
nshell = len(R_shell)
R_shell_f = np.fft.rfft(R_shell)/nshell
R_shell_f_r = R_shell_f.real
R_shell_f_i = R_shell_f.imag
Z_shell_f = np.fft.rfft(Z_shell)/nshell
Z_shell_f_r = Z_shell_f.real
Z_shell_f_i = Z_shell_f.imag
nwall = len(R_wall)
R_wall_f = np.fft.rfft(R_wall)/nwall
R_wall_f_r = R_wall_f.real
R_wall_f_i = R_wall_f.imag
Z_wall_f = np.fft.rfft(Z_wall)/nwall
Z_wall_f_r = Z_wall_f.real
Z_wall_f_i = Z_wall_f.imag
nR = len(R_shell_f)
nZ = len(Z_shell_f)
f = open('iterWinding_wall.txt','w')
'''
f.write('#		bmn		bnfp	nbf\n')
f.write("{:6d}{:6d}{:6d}\n".format(nR,1,0))
f.write('Current Surface\n')
f.write('n		m		rbc		rbs		zbc		zbs\n')
#f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(0,0,R_wall_f_r[0],R_wall_f_i[0],Z_wall_f_r[0],Z_wall_f_i[0]))
f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(0,0,R_shell_f_r[0],R_shell_f_i[0],Z_shell_f_r[0],Z_shell_f_i[0]))
for i in range(1,nR):
#	f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(0,i,2.*R_wall_f_r[i],-2.*R_wall_f_i[i],2.*Z_wall_f_r[i],-2.*Z_wall_f_i[i]))
	f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(0,i,2.*R_shell_f_r[i],-2.*R_shell_f_i[i],2.*Z_shell_f_r[i],-2.*Z_shell_f_i[i]))
'''
f.write('------ Current Surface: Coil-Plasma -------\n')
f.write('Number of fourier modes in table\n')
f.write(str(nR)+'\n')
f.write('Table of fourier coefficients\n')
f.write('m,n,crc2,czs2,crs2,czc2\n')
f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(0,0,R_wall_f_r[0],Z_wall_f_i[0],Z_wall_f_r[0],R_wall_f_i[0]))
#f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(0,0,R_shell_f_r[0],Z_shell_f_i[0],Z_shell_f_r[0],R_shell_f_i[0]))
for i in range (1,nR):
	f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(i,0,2.*R_wall_f_r[i],-2.*Z_wall_f_i[i],2.*Z_wall_f_r[i],-2.*R_wall_f_i[i]))
#	f.write("{:6d}{:6d}{:23.15E}{:23.15E}{:23.15E}{:23.15E} \n".format(i,0,2.*R_shell_f_r[i],-2.*Z_shell_f_i[i],2.*Z_shell_f_r[i],-2.*R_shell_f_i[i]))
f.close()
