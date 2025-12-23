import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy import signal

def noLinear(t_v, t, T_chirp, BW, kt, kb):
    
    # Parametros utilizados
    a = T_chirp*(1-kt)/2
    b = BW*(1-kb)/2
    # Pendiente de la parte lineal central
    M_1 = b/a

    # Puntos de corte temporal entre las funciones por partes
    t_3 = kt*T_chirp/2
    t_2 = T_chirp*(1 - kt/2)

    # Valores de la constante K de las funciones cuadraticas para garantizar su inicio y fin
    k_1 = ((BW/2)-M_1*t_3-b)/(t_3**2)
    k_3 = ((BW/2)-M_1*(T_chirp-t_2)-b)/((T_chirp-t_2)**2)

    # Funcion por partes
    f = sp.Piecewise(   (-k_1*(t_v-t_3)**2 + M_1*(t_v-t_3) - b,   t_v < t_3),
                        (M_1*(t_v-T_chirp/2),                     (t_v >= t_3) & (t_v <= t_2)),
                        (k_3*(t_v-t_2)**2 + M_1*(t_v-t_2) + b,    t_v > t_2 ))
    f_ = sp.lambdify(t_v, f)
    f_ = [f_(k) for k in t]

    # Fase instantanea de la señal Chirp (integral de la frecuencia instantánea)
    F = sp.integrate(f, t_v)

    F_num = sp.lambdify(t_v, F)
    phi = [F_num(v) for v in t]
    phi = np.array([float(i) for i in phi])

    # plt.plot(t, f_)
    # plt.show()

    return phi


def chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 0, mode_f = 0, alpha = 0, kt = 0.5, kb = 0.5): 
    
    # Cálculo del tiempo de Chirp
    T_chirp = dc*ipp/100

    # Número de puntos para la duración del Chirp
    n   = int(sr_tx*T_chirp) 

    # Arreglo de tiempos para la duración del Chirp [0 ... Trep]
    t = np.linspace(0, T_chirp, n)

    # Ventana de Blackman
    B = A*signal.windows.tukey(len(t), alpha)
    # Ventana de Chebyshev - 80 dB
    # atten = 80
    # B = A*signal.windows.chebwin(len(t), at=atten)
    # Ventana de Kaiser
    # beta = 8.6
    # B = A*signal.windows.kaiser(len(t), beta)

    # Definicion de variable de tiempo
    t_v = sp.symbols('t')

    # Forma de la señal Chirp:  A.exp(j.phi(t))
    #                           A.exp(j.phi(f))

    # Parametro M_ varia desde <0 , 1>
    phi = noLinear(t_v, t, T_chirp, bw, kt, kb)

    if mode_f == 1:
      # Trabajo con la variación en frecuencia
      r = int(sr_tx/sr_rx)
      phi = phi[::r]
      phi = [i for i in phi for _ in range(r)]
      phi = np.array(phi)

    # Fase instantánea en rad
    phi_rad = 2*np.pi*phi 
    
    # Señal solo Chirp generada
    chirp = B*np.exp(1j*phi_rad)

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

def testing ():

    A = 1
    ipp = 0.0004
    dc = 15
    sr_tx = 20000000
    sr_rx = 5000000
    fc = 0
    bw = 4000000
    t_d_ = 0
    mode_f_ = 0
    alpha_ =  1.0
    # Para obtener la forma de onda de la señal de referencia PX-1000, se debe cumplir: k_t < k_b
    k_t_ = 0.5
    k_b_ = 0.5

    chirp, full_chirp = chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = t_d_, mode_f = mode_f_, alpha = alpha_, kt = k_t_, kb = k_b_)  

    return chirp, full_chirp

if __name__ == "__main__":

    A = 1
    ipp = 0.0004
    dc = 15
    sr_tx = 20000000
    sr_rx = 5000000
    fc = 0
    bw = 4000000
    t_d_ = 0
    mode_f_ = 0
    alpha_ =  1.0
    # Para obtener la forma de onda de la señal de referencia PX-1000, se debe cumplir: k_t < k_b
    k_t_ = 0.5
    k_b_ = 0.5

    # Cálculo del tiempo de Chirp
    T_chirp = dc*ipp/100

    # Número de puntos para la duración del Chirp
    n   = int(sr_tx*T_chirp)

    chirp, full_chirp = chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = t_d_, mode_f = mode_f_, alpha = alpha_, kt = k_t_, kb = k_b_)
    t = np.linspace(0, T_chirp, n)

    plt.plot(t, np.real(chirp))
    plt.plot(t, np.imag(chirp))
    plt.show() 

