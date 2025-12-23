# Señal de Wels :)
import numpy as np
#import matplotlib.pyplot as plt

def generar_seno():

    frecuencia = 1000000
    amplitud = 1
    """
    Genera una señal seno.

    Parámetros:
    - frecuencia: Frecuencia de la señal en Hz
    - fs: Frecuencia de muestreo en Hz
    - duracion: Duración de la señal en segundos
    - amplitud: Amplitud de la señal (por defecto 1.0)

    Retorna:
    - t: Vector de tiempo
    - seno: Señal senoidal
    """
    duracion = 1.0
    fs = 20000000          # Frecuencia de muestreo (Hz)s
    t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)
    seno = amplitud * np.sin(2 * np.pi * frecuencia * t)
    return seno
    #return t,seno

# Generar una señal seno de 1 kHz, muestreada a 44.1 kHz, durante 1 segundo
#t, senal = generar_seno(100, 2.5)

#plt.plot(t, senal)
#plt.title("Señal Senoidal de 1 kHz")
#plt.xlabel("Tiempo [s]")
#plt.ylabel("Amplitud")
#plt.grid(True)
#plt.show()


