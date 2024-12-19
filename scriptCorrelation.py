import digital_rf as drf
import matplotlib.pyplot as plt
import numpy as np
import time

#do = drf.DigitalRFReader('/media/soporte/a9f70b3c-1295-40a4-ae80-96708705fdd0/test_final_many') #Ubicación donde se guardaran los archivo .hdf5
#chirp_tx = np.fromfile("/home/soporte/Descargas/many_chirp_ipp_0.0004_dc_15_sr_20000000_fc_0_bw_4000000.bin",dtype=np.complex64).tolist() #Ubicacion del archivo Chirp
do = drf.DigitalRFReader('/home/idi/data') #Ubicación donde se guardaran los archivo .hdf5
chirp_tx = np.fromfile("/home/idi/anaconda3/envs/sophy3.10/code/bin/chirp_amp_1_ipp_0.0004_dc_15_sr_20000000_fc_0_bw_4000000.bin",dtype=np.complex64).tolist() #Ubicacion del archivo Chirp
#print(do.get_channels())
s,e = do.get_bounds('ch0')
#print(s,e)

###---Parámetros modificables---###

IPP = 0.0004
sr = 20000000 ##Sample rate en RX
DC = 15/100
N = IPP*sr #Numero de puntos, visualización del IPP
i = N
N_chirp = DC*N

##--CHIRP--##
chirp = np.delete(chirp_tx,np.s_[int(N_chirp):])

##--RX--##
data = do.read_vector(s,i,'ch0')
data_i = np.imag(data)
data_i = np.where(np.abs(data_i)>30000,0,data_i)
data = np.real(data)
data = np.where(np.abs(data)>30000,0,data)

k = 0 #tiempo
time = np.empty(shape = [100,int(N)])
m = 0

##--Correlación--##
while True:
		graf = [0]
		data1 = do.read_vector(s,i,'ch0')
		#data1 = np.real(data1)
		data1 = data1[int(i-N):]
		data1 = np.where(np.abs(data1)>30000,0,data1)
		graf = np.correlate(data1,chirp,"same") #Same: mismo número de puntos (8000)
		t = np.linspace(0 + k*IPP*1e6,IPP*1e6 + k*IPP*1e6,len(graf))
		L = len(graf)
		NFFT = 4000.0 #Número de puntos
		X_rx = np.fft.fftshift((np.fft.fft(data1,int(NFFT))))
		X_corr = np.fft.fftshift((np.fft.fft(graf,int(NFFT))))
		f = np.linspace(-int(NFFT)/2,int(NFFT)/2-1,int(NFFT))*sr/NFFT # Vector de frecuencia 
		time[0] = abs(graf)
		
		####-------Potencia_C-------####
		
		P = X_corr*np.conj(X_corr)/(NFFT*NFFT)
		Pxx = P[[m]]
		m = m + 1	

		################################
		
		####--------Fourier_C-------####
	 	
		Fourier = np.abs(X_corr)/L #Normalizado
		
		################################
		
		####--------Gŕaficas--------####
		
		figure, axis = plt.subplots(2,2)
		axis[0,0].plot(t,data,label="Chirp Rx Real",color='green')
		axis[0,0].plot(t,data_i,label="Chirp Rx Imag",color='red')
		axis[0,0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
		axis[0,0].set_ylabel("x(t)",fontsize=10)
		axis[0,0].set_xlabel("Time(us)",fontsize=10)
		axis[0,0].grid(which = "both")
		axis[0,0].legend(loc=1,prop={'size': 13})
		axis[0,0].minorticks_on()
		axis[0,0].tick_params(which = "minor", bottom = False, left = False)
		
		axis[0,1].plot(f,abs(X_rx),label="Chirp Rx FFT")
		axis[0,1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
		axis[0,1].set_ylabel("Magnitude|X(f)|",fontsize=10)
		axis[0,1].set_xlabel("Frequency(Hz)",fontsize=10)
		axis[0,1].grid(which = "both")
		axis[0,1].legend(loc=1,prop={'size': 13})
		axis[0,1].minorticks_on()
		axis[0,1].tick_params(which = "minor", bottom = False, left = False)
		axis[0,1].set_xlim(-6e6,6e6)
		
		axis[1,0].plot(t,abs(graf),label="Correlation",color='blue')
		axis[1,0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
		axis[1,0].set_ylabel("c(t)",fontsize=10)
		axis[1,0].set_xlabel("Time(us)",fontsize=10)
		axis[1,0].grid(which = "both")
		axis[1,0].legend(loc=1,prop={'size': 13})
		axis[1,0].minorticks_on()
		axis[1,0].tick_params(which = "minor", bottom = False, left = False)
		
		axis[1,1].plot(f,Fourier,label="Correlation FFT",color='red')
		axis[1,1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
		axis[1,1].set_ylabel("Magnitude|C(f)|",fontsize=10)
		axis[1,1].set_xlabel("Frequency(Hz)",fontsize=10)
		axis[1,1].grid(which = "both")
		axis[1,1].legend(loc=1,prop={'size': 13})
		axis[1,1].minorticks_on()
		axis[1,1].tick_params(which = "minor", bottom = False, left = False)
		axis[1,1].set_xlim(-6e6,6e6)
		
		################################
		
		#plt.savefig('chirp_ipp_0.0004_dc_15_sr_20000000_fc_1000000_bw_1000000.jpg')	#Guardar figura: nombre
		print('Close plot ...')
		plt.show()
		
		z = input('Press "z" for exit: ')
		plt.close()
		
		i = i+N
		k = k+1
		
		if(z=='z'):
			break

for i in range (100):
	time[i] = time[0]

#print('time.shape: ',time.shape)
#print(time)

def Time():
	return time

