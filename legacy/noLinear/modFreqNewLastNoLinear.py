###---Modulación en Frecuencia con SDR para el radar meteorológico Sophy---###

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


"""
ChirpMod Inputs
- A             # Amplitud (valor unitario)
- ipp           # IPP (segundos)  
- dc            # DC (porcentaje %)
- sr_tx         # Sample rate en transmisión (Hz)
- sr_rx         # Sample rate en recepción (Hz)
- fc            # Frecuencia central (Hz)
- bw            # Ancho de banda (Hz)
- t_d           # Tiempo de desplazamiento Chirp (us)
- alpha         # alpha = <0,1>
                # alpha = 0: Ventana rectangular
                # alpha = 1: Ventana de Blackman
- mode_f        # Utilizado para trabajar con la variación de 
                  frecuencia cuando sr_tx y sr_rx son diferentes
                # mode_f = 0: Trabajo normal
                # mode_f = 1: Trabajo con la variación de frecuencia
- phi           # Angulo de desfase (rad)

ChirpMod Outputs
- chirp         # Arreglo 
                # solo de la señal Chirp
- full_chirp    # Arreglo 
                # de la señal Chirp completa (IPP)
"""


def chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 0, alpha = 0, mode_f = 0, phi = 0): 
    
    # Definición de las frecuencias superior e inferior
    f0_Hz = fc - bw/2.0
    f1_Hz = fc + bw/2.0

    # Cálculo del tiempo de Chirp
    T_chirp = dc*ipp/100.0

    # Chirp rate in Hz/s
    k   = bw/T_chirp

    # Número de puntos para la duración del Chirp
    n   = int(sr_tx*T_chirp)         	

    # Arreglo de tiempos para la duración del Chirp [0 ... Trep]
    t = np.linspace(0, T_chirp, n)

    # Ventana de Blackman
    B = A*signal.windows.tukey(n, alpha)

    # Frecuencia instantánea f(t) = k.t+f0
    f = k*t + f0_Hz

    # También: t = (f - f0_Hz)/k

    # Forma de la señal Chirp:  A.exp(j.phi(t))
    #                           A.exp(j.phi(f))

    # Trabajo con la variación en frecuencia
    if mode_f == 1:
      
      r = int(sr_tx/sr_rx)
 
      f = f[::r]
      f = [i for i in f for _ in range(r)]
      f = np.array(f)

    # Fase instantanea de la señal Chirp (integral de la frecuencia instantánea)
    # phi = (k*t/2 + f0_Hz)*t

    # Tomando en cuenta t = (f - f0_Hz)/k
    # phi_f = (f/2.0 + f0_Hz/2.0)*(f - f0_Hz)/k
    phi_f = (t**2)*k/2 + t*f0_Hz

    # Fase instantánea en rad
    phi_rad = 2*np.pi*phi_f 

    # Señal solo Chirp generada
    chirp = B*np.exp(1j*(phi_rad + phi))

    # N: Número de muestras total (IPP)
    N = n*100/dc

    # N_z: Número de muestras sobrantes (igual a 0)
    N_z = N - n

    # Señal Chirp con ceros para completar el IPP
    full_chirp = np.hstack((chirp, np.zeros(int(N_z))))
    
    # Desplazamiento de la señal Chirp
    N_d = int(N*t_d/(ipp*1000000))

    full_chirp = np.roll(full_chirp, N_d)

    return chirp, full_chirp


def plotting(array, time):

    plt.plot(time, array)
    plt.show()

# Ejemplo
if __name__ == "__main__":
  
  A = 1
  ipp = 0.0004
  dc = 15
  sr_tx = 20000000
  sr_rx = 5000000
  # La frecuencia central definirá el barrido Chirp (ascendente o descendente)
  fc = 0
  bw = 5000000
  td_ = 0
  alpha_ = 1.0
  mode_f_ = 0
  phi_ = 0

  chirp, full_chirp = chirpMod(A, ipp, dc, sr_rx, sr_rx, fc, bw, t_d = td_, alpha = alpha_, mode_f = mode_f_, phi = phi_)
  t = [i for i in range(len(chirp))] 

  plt.plot(t, np.real(chirp))
  plt.plot(t, np.imag(chirp)) 
  plt.show() 
