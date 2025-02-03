import digital_rf as drf
import matplotlib.pyplot as plt
import numpy as np
import time
import argparse
import re

###---Define Chirp Signal Parameters---###

parser = argparse.ArgumentParser(description = '###---Correlation Chirp Signal---###')

parser.add_argument('-file_ch','--file_channel',dest='file_channel',type=str,default=None,help='''Channel File''')
parser.add_argument('-file_bin','--final_binary',dest='file_binary',type=str,default=None,help='''Binary File''')

args = parser.parse_args()

file_ch_ = args.file_channel
file_bin_ = args.file_binary

patron = r"ipp_(\d+\.\d+)_dc_(\d+\.\d+)_sr_(\d+\.\d+)"
coincidencia = re.search(patron, file_bin_)

if coincidencia:
    ipp = float(coincidencia.group(1))
    dc = float(coincidencia.group(2))
    sr = float(coincidencia.group(3))

do = drf.DigitalRFReader(file_ch_) 								# Ubicación donde se guardaran los archivo .hdf5
chirp_tx = np.fromfile(file_bin_,dtype=np.complex64).tolist() 	# Ubicacion del archivo Chirp

# do = drf.DigitalRFReader('/home/idi/data') #Ubicación donde se guardaran los archivo .hdf5
# Ubicacion del archivo Chirp
# chirp_tx = np.fromfile("/home/idi/anaconda3/envs/sophy3.10/code/bin/chirp_amp_1.0_ipp_0.0004_dc_15.0_sr_20000000.0_fc_0.0_bw_4000000.0.bin",dtype=np.complex64).tolist() 

s,e = do.get_bounds('ch0')
# print(do.get_channels())
# print(s,e)

###---Parámetros modificables---###

IPP = ipp
SR = sr 		# Sample rate en RX
DC = dc/100
N = IPP*sr 		# Numero de puntos, visualización del IPP
N_chirp = DC*N
i = N

###---CHIRP---###
chirp = np.delete(chirp_tx, np.s_[int(N_chirp):])

###---RX---###
data = do.read_vector(s, i, 'ch0')
data_i = np.imag(data)
data_i = np.where(np.abs(data_i)>30000,0,data_i)
data = np.real(data)
data = np.where(np.abs(data)>30000,0,data)

k = 0 # Tiempo
time = np.empty(shape = [100,int(N)])
m = 0

###---Correlación---###
while True:
		graf = [0]
		data1 = do.read_vector(s,i,'ch0')
		# data1 = np.real(data1)
		data1 = data1[int(i-N):]
		data1 = np.where(np.abs(data1)>30000,0,data1)
		graf = np.correlate(data1,chirp,"same") 						# Same: mismo número de puntos (8000)
		t = np.linspace(0 + k*IPP*1e6,IPP*1e6 + k*IPP*1e6,len(graf))
		L = len(graf)
		NFFT = 4000.0 													# Número de puntos
		X_rx = np.fft.fftshift((np.fft.fft(data1,int(NFFT))))
		X_corr = np.fft.fftshift((np.fft.fft(graf,int(NFFT))))
		f = np.linspace(-int(NFFT)/2,int(NFFT)/2-1,int(NFFT))*SR/NFFT 	# Vector de frecuencia 
		time[0] = abs(graf)
		
		####-------Potencia_C-------####
		
		P = X_corr*np.conj(X_corr)/(NFFT*NFFT)
		Pxx = P[[m]]
		m = m + 1
		
		####--------Fourier_C-------####
	 	
		Fourier = np.abs(X_corr)/L 										#Normalizado
		
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

def Time():
	return time

# Usado ahora
# python3 scriptCorrelation.py -file_ch /home/idi/data -file_bin /home/idi/anaconda3/envs/sophy3.10/code/bin/chirp_amp_1.0_ipp_0.0004_dc_15.0_sr_20000000.0_fc_2000000.0_bw_4000000.0.bin