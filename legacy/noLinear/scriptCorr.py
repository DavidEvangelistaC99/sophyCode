import matplotlib.pyplot as plt
import numpy as np
import test_NLFM    
import NLFM

# Correlacion en el tiempo

def corrTime (data1, data2, NFFT = 100):

    corr = np.correlate(data1, data2, mode='full')

    time_ = [j for j in range(len(corr))]
    plt.plot(time_, np.abs(corr))
    plt.show()

    corr_freq = np.fft.fftshift((np.fft.fft(corr, int(NFFT))))

    freq_ = [i for i in range(len(corr_freq))]
    plt.plot(freq_, abs(corr_freq))
    plt.show()


# Ejemplo
if __name__ == "__main__":
  
    chirppy, _ = NLFM.testing()
    t = [i for i in range(len(chirppy))]

    plt.plot(t, np.real(chirppy))
    plt.plot(t, np.imag(chirppy))
    plt.show()

    corrTime(chirppy, chirppy, 1200)
