import numpy as np
def read_plabry_bn(file_name):
	fo = open(file_name, 'r')
	line = fo.readline()
	line = fo.readline()
	plabry_harmonics = int(line.split()[0])	
	bn_harmonics = int(line.split()[2])
	line = fo.readline()
	line = fo.readline()
	plabry_array = np.zeros((plabry_harmonics,6))
	for i in range(plabry_harmonics):
		line = fo.readline()
		element = line.split()
		for j in range(6):
			plabry_array[i,j] = element[j]
	
	line = fo.readline()
	line = fo.readline()
	bn_array = np.zeros((bn_harmonics,4))
	for i in range((bn_harmonics)):
		line = fo.readline()
		element = line.split()
		for j in range(4):
			bn_array[i,j] = element[j]
	fo.close()
	return plabry_harmonics,bn_harmonics,plabry_array,bn_array
	

def read_surface_iter(file_name):
	fo = open(file_name, 'r')
	line = fo.readline()
	line = fo.readline()
	line = fo.readline()
	nharmonics = int(line)	
	line = fo.readline()
	line = fo.readline()
	read_array = np.zeros((nharmonics,6))
	for i in range(nharmonics):
		line = fo.readline()
		element = line.split()
		for j in range(6):
			read_array[i,j] = element[j]
	fo.close()
	return nharmonics, read_array

def read_surface_d3d(file_name):
    fo = open(file_name, 'r')
    line = fo.readline()
    line = fo.readline()
    nharmonics = int(line.split()[0])
    line = fo.readline()
    line = fo.readline()
    read_array = np.zeros((nharmonics,6))
    for i in range(nharmonics):
        line = fo.readline()
        element = line.split()
        for j in range(6):
            read_array[i,j] = element[j]
	fo.close()
    return nharmonics, read_array

def windsuf_iter3d(nharmonics,coeff_array,polAng,torAng):
	ntor = len(torAng) 
	npol = len(polAng)
	polAng,torAng = np.meshgrid(polAng,torAng)	
	RR = np.zeros((ntor,npol))
	ZZ = np.zeros((ntor,npol))
	XX = np.zeros((ntor,npol))
	YY = np.zeros((ntor,npol))
	mnum = coeff_array[:,0]
	nnum = coeff_array[:,1]
	crc  = coeff_array[:,2]
	crs  = coeff_array[:,4]
	czc  = coeff_array[:,5]
	czs  = coeff_array[:,3]
	for i in range(ntor):
		for j in range(npol):
			for k in range(nharmonics):
				angle = mnum[k]*polAng[i,j] + nnum[k]*torAng[i,j]
				RR[i,j] = RR[i,j] + crc[k]*np.cos(angle) + crs[k]*np.sin(angle)
				ZZ[i,j] = ZZ[i,j] + czc[k]*np.cos(angle) + czs[k]*np.sin(angle)
			XX[i,j] = RR[i,j]*np.cos(torAng[i,j])
			YY[i,j] = RR[i,j]*np.sin(torAng[i,j])
	
	return XX, YY, RR, ZZ

def windsuf_iter2d(nharmonics,coeff_array,polAng,torAng):
	ntor = len(torAng)
	npol = len(polAng)
	if ntor != npol:
		print('Toroidal and poloidal angles have to be the same length')
	else:
		RR = np.zeros(ntor)
		ZZ = np.zeros(ntor)
		XX = np.zeros(ntor)
		YY = np.zeros(ntor)
		mnum = coeff_array[:,0]
		nnum = coeff_array[:,1]
		crc  = coeff_array[:,2]
		crs  = coeff_array[:,4]
		czc  = coeff_array[:,5]
		czs  = coeff_array[:,3]
		for i in range(ntor):
			for k in range(nharmonics):
				angle = mnum[k]*polAng[i,j] + nnum[k]*torAng[i,j]
				RR[i,j] = RR[i,j] + crc[k]*np.cos(angle) + crs[k]*np.sin(angle)
				ZZ[i,j] = ZZ[i,j] + czc[k]*np.cos(angle) + czs[k]*np.sin(angle)
			XX[i] = RR[i]*np.cos(torAng[i])
			YY[i] = RR[i]*np.sin(torAng[i])
	return XX, YY, RR, ZZ

def plabry_and_bn_3d(file_name,polAng,torAng):
	nfourier_bry,nfourier_bn,plabry_array,bn_array = read_plabry_bn(file_name) 
	ntor = len(torAng)
	npol = len(polAng) 
	polAng,torAng = np.meshgrid(polAng,torAng)
	RR = np.zeros((ntor,npol))
	ZZ = np.zeros((ntor,npol))
	XX = np.zeros((ntor,npol))
	YY = np.zeros((ntor,npol))

	m_bry = plabry_array[:,1]
	n_bry = plabry_array[:,0]
	crc  = plabry_array[:,2]
	crs  = plabry_array[:,3]
	czc  = plabry_array[:,4]
	czs  = plabry_array[:,5]

	BB = np.zeros((ntor,npol))
	m_bn = bn_array[:,0]
	n_bn = bn_array[:,1]
	bnc  = bn_array[:,2]
	bns  = bn_array[:,3]

	for i in range(ntor):
		for j in range(npol):
			for k in range(nfourier_bry):
				angle = m_bry[k]*polAng[i,j] + n_bry[k]*torAng[i,j]
				RR[i,j] = RR[i,j] + crc[k]*np.cos(angle) + crs[k]*np.sin(angle)
				ZZ[i,j] = ZZ[i,j] + czc[k]*np.cos(angle) + czs[k]*np.sin(angle)
			XX[i,j] = RR[i,j]*np.cos(torAng[i,j])
			YY[i,j] = RR[i,j]*np.sin(torAng[i,j])

			for kk in range(nfourier_bn):
				angle = m_bn[k]*polAng[i,j] + n_bn[k]*torAng[i,j]
				BB[i,j] = BB[i,j] + bnc[k]*np.cos(angle) + bns[k]*np.sin(angle)
	return XX, YY, RR, ZZ, BB
