###---Modulación en Frecuencia con SDR para el radar meteorológico Sophy---###

import numpy as np

def chirpStandard(A, fs_Hz, rep_Hz, f0_Hz, f1_Hz, phase_rad = 0, mode = 1):      ##rep_Hz inversa De la duracion del CHIRP
    T_rep = 1/rep_Hz                 	# Periodo CHIRP.             //Tiempo de duración del CHIRP
    k   = (f1_Hz - f0_Hz)/T_rep        	# Chirp rate in Hz/s.        //CHIRP rate indepenediente de lo demás
    n   = int(fs_Hz/rep_Hz)          	# Samples per repetition.    //Número de puntitos en la duración del CHIRP

    if mode==0:
      t_s = np.linspace(0,T_rep,n)   	# Chirp Sample times.        //Arreglo de tiempos para la duración del CHIRP [0 ... Trep]
    else:
      t_s = np.linspace(-T_rep/2.0,T_rep/2.0,n)

    # Phase,phi_Hz, is integral of frequency, f(t)=kt/2+f0
    phi_Hz  = (k*t_s/2.0+f0_Hz)*t_s  	# PHISTANTENEA               //f(t)*t
    phi_rad = 2*np.pi*phi_Hz         	# Convert to radians         //Argumento de la señal CHIRP
    phi_rad += phase_rad             	# Offser by user-specified inital phase
    #return  t_s,A*np.exp(1j*phi_rad),T_rep,n
    return t_s,A*np.exp(1j*phi_rad),T_rep,n
    #return t_s,A*np.sin(phi_rad),T_rep,n  #ust real or I, component.

##------##
def chirpCentral(A,fs_Hz,fc_Hz,rep_Hz,bw_Hz,phase_rad=0,mode=0):
     f0_Hz = fc_Hz - bw_Hz/2.0
     f1_Hz = fc_Hz + bw_Hz/2.0
     print("Band Width: ",bw_Hz, "Hz")
     print("f0: ",f0_Hz, "Hz")
     print("f1: ",f1_Hz, "Hz")
     
     return chirpStandard(A,fs_Hz=fs_Hz,rep_Hz=rep_Hz,f0_Hz=f0_Hz,f1_Hz=f1_Hz,mode=mode)

"""

#CHIRP
#-Parameters-#

IPP = 100/30               ##seconds
DC = 15                    ##percent %
f_central = 150            #Hz
samp_rate = 2000           #Hz
B1 = DC*samp_rate/100      #Hz

"""

def chirp_mod(A,ipp,dc,sr,fc,b):
  f_s = sr
  f_c = fc
  T_rep = dc*ipp/100
  rep_Hz = 1/T_rep
  B = b 
  
  return chirpCentral(A,f_s,f_c,rep_Hz,B)
  
"""

CHIRP USRP


"""
def chirp_usrp(A,ipp,dc,sr,fc,b):
  t_c,chirp_m,T_c,N = chirp_mod(A,ipp,dc,sr,fc,b)
  n_3 = N*100/dc
  n_2 = n_3-N
  mod_chirp_ = np.hstack((chirp_m,np.zeros(int(n_2))))

  return mod_chirp_

