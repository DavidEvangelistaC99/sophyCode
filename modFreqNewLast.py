###---Modulacion en Frecuencia con SDR para el radar meteorologico Sophy---###

import numpy as np
from scipy import signal
# import matplotlib.pyplot as plt


"""
ChirpMod Inputs
- A             # Amplitud (valor unitario)
- ipp           # IPP (segundos)  
- dc            # DC (porcentaje %)
- sr_tx         # Sample rate en transmision (MHz)
- sr_rx         # Sample rate en recepcion (MHz)
- fc            # Frecuencia central (Hz)
- bw            # Ancho de banda (MHz)
- t_d           # Tiempo de desplazamiento Chirp (us)
- window        # Tipo de ventana "R", "K", "B"
                # window = "R": Ventana rectangular
                # window = "K": Ventana de Kaiser 70 dB
                # window = "B": Ventana Blackman
- mode_f        # Utilizado para trabajar con la variacion de 
                  frecuencia cuando sr_tx y sr_rx son diferentes
                # mode_f = 0: Trabajo normal
                # mode_f = 1: Trabajo con la variacion de frecuencia
- phi           # Angulo de desfase (rad)

ChirpMod Outputs
- chirp         # Arreglo 
                # solo de la senal Chirp
- full_chirp    # Arreglo 
                # de la senal Chirp completa (IPP)
"""


def chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 0, window = 'R', mode_f = 0, phi = 0): 
    
    # Definicion de las frecuencias superior e inferiors
    f0_Hz = fc - bw/2.0
    f1_Hz = fc + bw/2.0

    # Calculo del tiempo de Chirp
    T_chirp = dc*(ipp)/100.0

    # Chirp rate in Hz/s
    k   = bw/T_chirp

    # Numero de puntos para la duracion del Chirp
    n   = int(sr_tx*T_chirp)         	

    # Arreglo de tiempos para la duracion del Chirp [0 ... Trep]
    t = np.linspace(0, T_chirp, n)

    if window == 'K':
      # Valor de beta para una atenuacion de 70 dB
      beta = signal.kaiser_beta(70)
      B = A*signal.windows.kaiser(n, beta)
    else:
      if window == 'B':
        # Valor 1.0 para ventana de Kaiser
        alpha = 1.0
        B = A*signal.windows.tukey(n, alpha)
      else:
        B = A

    # Frecuencia instantanea f(t) = k.t+f0
    f = k*t + f0_Hz

    # Tambien: t = (f - f0_Hz)/k

    # Forma de la senal Chirp:  A.exp(j.phi(t))
    #                           A.exp(j.phi(f))

    # Trabajo con la variacion en frecuencia (parametro mode_f)
    if mode_f == 1:
      
      r = int(sr_tx/sr_rx)
 
      f = f[::r]
      f = [i for i in f for _ in range(r)]
      f = np.array(f)

    # Fase instantanea de la senal Chirp (integral de la frecuencia instantanea)
    # phi = (k*t/2 + f0_Hz)*t

    # Tomando en cuenta t = (f - f0_Hz)/k
    # phi_f = (f/2.0 + f0_Hz/2.0)*(f - f0_Hz)/k
    phi_f = (t**2)*k/2 + t*f0_Hz

    # Fase instantanea en rad
    phi_rad = 2*np.pi*phi_f 

    # Senal solo Chirp generada
    chirp = B*np.exp(1j*(phi_rad + phi))

    # N: Numero de muestras total (IPP)
    N = n*100/dc

    # N_z: Numero de muestras sobrantes (igual a 0)
    N_z = N - n

    # Senal Chirp con ceros para completar el IPP
    full_chirp = np.hstack((chirp, np.zeros(int(N_z))))
    
    # Desplazamiento de la senal Chirp
    N_d = int(N*t_d/(ipp*1.0e6))

    # Senal Chirp completa (IPP) generada
    full_chirp = np.roll(full_chirp, N_d)

    return chirp, full_chirp


# Funcion para el doble pulso Chirp (de acuerdo con el articulo de referencia PX1000)
def chirpModUnion_1(ipp, sr_tx, sr_rx, A_1, A_2, dc_1, dc_2, fc_1, fc_2, bw_1, bw_2, t_d_, window_1, window_2):
    
    _, full_chirp_1 = chirpMod(A_1, ipp, dc_1, sr_tx, sr_rx, fc_1, bw_1, t_d = t_d_, window = window_1, mode_f = 0)
    _, full_chirp_2 = chirpMod(A_2, ipp, dc_2, sr_tx, sr_rx, fc_2, bw_2, t_d = t_d_ + dc_1*ipp*(1e6/1e2), window = window_2, mode_f = 0)
    full_chirp = np.array(full_chirp_1) + np.array(full_chirp_2)

    return full_chirp


# Funcion para el doble pulso Chirp (de acuerdo con la forma de envio actual CC)
def chirpModUnion_2(ipp, sr_tx, sr_rx, A_1, A_2, dc_1, dc_2, fc_1, fc_2, bw_1, bw_2, t_d_, window_1, window_2, rep_1 = 1, rep_2 = 1):
    
    _, full_chirp_1 = chirpMod(A_1, ipp, dc_1, sr_tx, sr_rx, fc_1, bw_1, t_d = t_d_, window = window_1, mode_f = 0)
    _, full_chirp_2 = chirpMod(A_2, ipp, dc_2, sr_tx, sr_rx, fc_2, bw_2, t_d = t_d_, window = window_2, mode_f = 0)

    full_chirp_1 = np.tile(full_chirp_1, int(rep_1))
    full_chirp_2 = np.tile(full_chirp_2, int(rep_2))
    full_chirp = np.concatenate((full_chirp_1, full_chirp_2))

    return full_chirp


# Ejemplo
if __name__ == "__main__":
  
  A = 1.0
  ipp = 400.0e-6
  dc = 12.0
  sr_tx = 20.0e6
  sr_rx = 2.5e6
  # La frecuencia central definirá el barrido Chirp (ascendente o descendente)
  fc = 0.0e6
  bw = 1.0e6
  td_ = 5.2
  window_ = 'B'
  mode_f_ = 0
  phi_ = 0
  rep_ = 250.0

  # chirp, full_chirp = chirpMod(A, ipp, dc, sr_rx, sr_rx, fc, bw, t_d = td_, window = window_, mode_f = mode_f_, phi = phi_)

  # chirpModUnion_1(ipp, sr_tx, sr_rx, A_1, A_2, dc_1, dc_2, fc_1, fc_2, bw_1, bw_2, t_d_, window_1, window_2)
  # full_chirp_1 = chirpModUnion_1(ipp, sr_tx, sr_rx, A, A, 12.0, 12.0, 0.0e6, 2.0e6, 1.0e6, 0.0e6, td_, 'B', 'R')
  
  # chirpModUnion_2(ipp, sr_tx, sr_rx, A_1, A_2, dc_1, dc_2, fc_1, fc_2, bw_1, bw_2, t_d_, window_1, window_2, rep_1, rep_2)
  # full_chirp_2 = chirpModUnion_2(ipp, sr_rx, sr_rx, A, A/2.0, dc, 1.0, fc, fc, bw, bw, td_, window_, 'R', rep_, rep_)
  
  # t = [i for i in range(len(full_chirp_1))] 
  # plt.plot(t, np.real(full_chirp_1)) 
  # plt.plot(t, np.imag(full_chirp_1)) 
  # plt.show() 
