import modFreqNewLast as modf
import matplotlib.pyplot as plt
import numpy as np

# Espectro de potencia de la señal recibida

def spectraPower (data1, NFFT = 100):

    power = np.fft.fftshift((np.fft.fft(data1, int(NFFT))))
    freq_ = np.linspace(-int(NFFT)/2, int(NFFT)/2-1, int(NFFT))*(5000000/NFFT)

    plt.plot(freq_, abs(power))
    plt.show()

# Correlacion en el tiempo

def corrTime (data1, data2, NFFT = 100):

    corr = np.correlate(data1, data2, mode='same')

    time_ = [j for j in range(len(corr))]
    plt.plot(time_, np.abs(corr))
    plt.show()

    corr_freq = np.fft.fftshift((np.fft.fft(corr, int(NFFT))))

    freq_ = [i for i in range(len(corr_freq))]
    plt.plot(freq_, abs(corr_freq))
    plt.show()

# Ejemplo
if __name__ == "__main__":

    chirppy, _ = modf.testing()
    t = [i for i in range(len(chirppy))]

    plt.plot(t, np.real(chirppy))
    plt.plot(t, np.imag(chirppy))
    plt.show()

    # spectraPower (chirppy, 1200)
    corrTime(chirppy, chirppy, 1200)
