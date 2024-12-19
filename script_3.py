import digital_rf as drf
import matplotlib.pyplot as plt
import numpy as np
import time

##--Ubicación script_2_correalte.py--## 
do = drf.DigitalRFReader('/media/soporte/a9f70b3c-1295-40a4-ae80-96708705fdd0/data') #Ubicación donde se guardaran los archivo .hdf5
chirp_tx = np.fromfile("/home/soporte/Descargas/script/chirp_amp_1_ipp_0.0004_dc_15_sr_20000000_fc_0_bw_4000000.bin",dtype=np.complex64).tolist() #Ubicacion del archivo Chirp
#print(do.get_channels())
s,e = do.get_bounds('ch0')
#print(s,e)

IPP = 0.0004
sr = 20000000	##Sample rate en RX
DC = 15/100
N = IPP*sr 	#Numero de puntos, visualización del IPP
i = N
N_chirp = DC*N

##--CHIRP--##
chirp = np.delete(chirp_tx, np.s_[int(N_chirp):])

##--RX--##
data = do.read_vector(s,i,'ch0')
#data = np.real(data)
data = np.where(np.abs(data)>30000,0,data)

k = 0 #tiempo
time = np.empty(shape = [100,int(N)])
m = 0

##--Correlación--##
while m<1:
		graf=[0]
		data1 = do.read_vector(s,i,'ch0')
		#data1 = np.real(data1)
		data1 = data1[int(i-N):]
		data1 = np.where(np.abs(data1)>30000,0,data1)
		graf = np.correlate(data1,chirp,"same")	#Correlación!!!!!
		time[0] = graf*np.conj(graf) 		#OJO Espectrograma 
		#print(len(time[0]))
		
		###---Gráfica---###
		
		#t = np.linspace(0,IPP,len(graf))
		#plt.plot(t,graf)
		#plt.grid()
		#plt.show()
		
		###################
		
		m = m + 1
		
for i in range (100):
	time[i] = time[0]

#print('time.shape: ',time.shape)
#print(time)

def Time():
	return time

