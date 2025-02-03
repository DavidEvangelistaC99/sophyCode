###---Modulación en Frecuencia con SDR para el radar meteorológico Sophy---###

import numpy as np
import matplotlib.pyplot as plt

def chirpStandard(A, fs_Hz, rep_Hz, f0_Hz, f1_Hz, phase_rad = 0, mode = 1): 
    # Periodo CHIRP
    T_rep = 1/rep_Hz 
    # Chirp rate in Hz/s
    k   = (f1_Hz - f0_Hz)/T_rep 
    # Número de puntos para la duración del CHIRP
    n   = int(fs_Hz/rep_Hz)          	

    # Arreglo de tiempos para la duración del CHIRP [0 ... Trep]
    if mode==0:
      t_s = np.linspace(0, T_rep, n)         
    else:
      t_s = np.linspace(-T_rep/2.0, T_rep/2.0, n)
 
    # Fase instantánea f(t)=kt/2+f0
    phi_Hz  = (k*t_s/2.0 + f0_Hz)*t_s 
    phi_rad = 2*np.pi*phi_Hz         	         
    # Argumento de la señal CHIRP
    phi_rad += phase_rad             	

    return t_s,A*np.exp(1j*phi_rad),T_rep,n

    # Envío de componente solo real o imaginario
    # return t_s,A*np.sin(phi_rad),T_rep,n 

def chirpCentral(A, fs_Hz, fc_Hz, rep_Hz, bw_Hz, phase_rad = 0, mode = 0):
     f0_Hz = fc_Hz - bw_Hz/2.0
     f1_Hz = fc_Hz + bw_Hz/2.0
     # print("Band Width: ",bw_Hz, "Hz")
     # print("f0: ",f0_Hz, "Hz")
     # print("f1: ",f1_Hz, "Hz")
     
     return chirpStandard(A, fs_Hz = fs_Hz, rep_Hz = rep_Hz, f0_Hz = f0_Hz, f1_Hz = f1_Hz, mode = mode)

def chirpMod(A, ipp, dc, sr, fc, b):
  f_s = sr
  f_c = fc
  T_rep = dc*ipp/100
  rep_Hz = 1/T_rep
  B = b 
  
  return chirpCentral(A, f_s, f_c, rep_Hz, B)
  
"""
CHIRP USRP
Parameters

IPP           #seconds s
DC            #percent %
f_central     #Hz
samp_rate     #Hz
B1            #Hz
"""

def chirpUsrp(A, ipp, dc, sr, fc, b):
  t_c, chirp_m, T_c, N = chirpMod(A, ipp, dc, sr, fc, b)
  n_3 = N*100/dc
  n_2 = n_3 - N
  mod_chirp_ = np.hstack((chirp_m,np.zeros(int(n_2))))

  return mod_chirp_

def shiftChirpUsrp(A, ipp, dc, sr, fc, b, t=-1):
  t_c, chirp_m, T_c, N = chirpMod(A, ipp, dc, sr, fc, b)
  n_3 = N*100/dc
  n_2 = n_3 - N

  if t>=0:
    mod_chirp_ = np.hstack((chirp_m,np.zeros(int(n_2))))
    n = int(sr*t/1000000)
    n = n % len(mod_chirp_)
    return mod_chirp_[n:] + mod_chirp_[:n]
  
  else:
    return mod_chirp_

if __name__ == "__main__":
  
  A = 1
  ipp = 0.0004
  dc = 15
  sr = 20000000
  fc = 2000000
  b = 4000000
      
  chirp = shiftChirpUsrp(A, ipp, dc, sr, fc, b, 400)
  t = np.arange(len(chirp))
  print(chirp)

  plt.plot(t, np.real(chirp))
  plt.show()