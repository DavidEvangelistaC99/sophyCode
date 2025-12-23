import digital_rf as drf
import matplotlib.pyplot as plt
import numpy as np
from modFreqNewLast import chirpMod

############################################################
# Espectro de potencia de la señal recibida

def spectraPower (data1, NFFT = 100):
    power = np.fft.fftshift((np.fft.fft(data1, int(NFFT))))
    # power = np.fft.fftshift(np.fft.fft(data1))
    print("Longitud de FFT: ", len(power))

    freq_ = np.linspace(-int(NFFT)/2, int(NFFT)/2-1, int(NFFT))*(SR_RX/NFFT)
    # freq_ = [i for i in range(len(power))]

    plt.plot(freq_, abs(power))
    plt.show()

############################################################
# Correlacion en el tiempo

def corrTime (data1, data2, NFFT = 100):

    corr = np.correlate(data1, data2, mode='same')

    print("Longitud de la correlacion obtenida: ", len(corr))

    time_ = [j for j in range(len(corr))]
    
    plt.plot(time_, np.abs(corr))
    plt.show()

    corr_freq = np.fft.fftshift((np.fft.fft(corr, int(NFFT))))

    # corr_freq = np.fft.fft(corr, int(NFFT))
    # corr_freq = np.fft.fft(corr)
    
    # corr_freq[len(corr_freq)//2] = 0
    # freq = np.fft.fftfreq(len(corr_freq))
    # freq_ = np.linspace(-int(NFFT)/2, int(NFFT)/2-1, int(NFFT))*(SR_RX/NFFT) 
    freq_ = [i for i in range(len(corr_freq))]

    plt.plot(freq_, abs(corr_freq))
    plt.show()

############################################################
# Correlación en frecuencia

def corrFreq (data1, data2, NFFT=100):

    freq_1 = np.fft.fft(data1)
    freq_2 = np.fft.fft(data2)
    corr = np.conj(freq_1)*freq_2
    freq_ = [i for i in range(len(corr))]

    plt.plot(freq_, corr)
    plt.show()

    corr_time = np.fft.ifft(corr)
    time_ = [i for i in range(len(corr_time))]

    plt.plot(time_, abs(corr_time))
    plt.show()


# Ejemplo
if __name__ == "__main__":
  
    # Ubicación donde se guardan los archivo .hdf5
    do = drf.DigitalRFReader('/home/idi/data_freq/pruebas/fc_0') 

    A = 1.0
    ipp = 0.0004
    dc = 15
    sr_tx = 20000000
    sr_rx = 5000000
    fc = 0
    bw = 4000000

    # Le tenemos que enviar o reemplazar sr_tx = 20000000 o tambien sr_tx = sr_rx
    chirp_tx, chirp_tx_ = chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 0, alpha = 1.0, mode_f = 0)

    print("Longitud de la chirp binario TX: ", len(chirp_tx))

    time_1 = [j for j in range(len(chirp_tx))]

    plt.plot(time_1, np.real(chirp_tx))
    plt.plot(time_1, np.imag(chirp_tx))
    plt.show()

    ############################################################

    # Parámetros 
    IPP = 0.0004
    SR_TX = 20000000		# Sample rate en TX
    SR_RX = 5000000         # Sample rate en RX
    DC = 15/100
    N = IPP*SR_RX			# Numero de puntos, visualización del IPP
    N_CHIRP = DC*N

    ############################################################

    s, e = do.get_bounds('ch0')
    data = do.read_vector(s, N, 'ch0')
    data = np.where(np.abs(data)>30000, 0, data)

    print("Numero de puntos de la chirp RX: ", len(data))

    time_2 = [j for j in range(len(data))]

    plt.plot(time_2, np.real(data))
    plt.plot(time_2, np.imag(data))
    # plt.plot(time_2, np.abs(data))
    plt.show()

    # spectraPower(chirp_tx, 2000)
    # spectraPower(data, 2000)
    # Debemos considerar el numero de puntos del tiempo de transmision para el procesos de FFT en corrTime
    corrTime(chirp_tx, chirp_tx, 1200)
