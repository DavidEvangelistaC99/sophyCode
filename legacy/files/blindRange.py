import numpy as np
import matplotlib.pyplot as plt
from modFreqNewLast import chirpMod

def generateUnion():
    # Test 1 para el envio de la union Chirp
    A = 1
    ipp = 0.0004
    dc = 0.4
    sr_tx = 20000000
    sr_rx = 5000000
    # La frecuencia central definirá el barrido Chirp (ascendente o descendente)
    fc = -1100000
    bw = 2200000
    # td_ = 0.0
    alpha_ = 1.0
    mode_f_ = 1

    chirp1, full_chirp1 = chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 0.0, window = 'b', mode_f = mode_f_)
    chirp2, full_chirp2 = chirpMod(0.5, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 200.0, window = 'r', mode_f = mode_f_)
    
    full_chirp = np.array(full_chirp1) + np.array(full_chirp2)

    return full_chirp

def generateDesphase():
    # Test 2 para el envio de la union Chirp (prueba de desfase) 
    A = 1
    ipp = 0.0004
    dc = 0.1
    sr_tx = 20000000
    sr_rx = 5000000
    # La frecuencia central definirá el barrido Chirp (ascendente o descendente)
    fc = -1100000
    bw = 2200000
    alpha_ = 1.0
    mode_f_ = 0
    phi_ = np.pi

    chirp1, full_chirp1 = chirpMod(A, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 0.0, alpha = alpha_, mode_f = mode_f_)
    chirp2, full_chirp2 = chirpMod(0.5, ipp, dc, sr_tx, sr_rx, fc, bw, t_d = 200.0, alpha = alpha_, mode_f = mode_f_, phi = phi_)
    
    full_chirp = np.array(full_chirp1) + np.array(full_chirp2)

    return full_chirp

def generateBlind():
    # Test para el envio de la union Chirp (referencia)
    # Constantes para cada señal
    ipp = 0.0004
    sr_tx = 20000000
    sr_rx = 5000000
    mode_f_ = 0
    phase = 0

    # Variables para cada señal
    A_1 = 1
    A_2 = 1
    dc_1 = 10
    dc_2 = 0.4
    fc_1 = -750000
    bw_1 = 1500000
    fc_2 = -1250000
    bw_2 = 2500000
    
    _, full_chirp1 = chirpMod(A_1, ipp, dc_1, sr_tx, sr_rx, fc_1, bw_1, t_d = 0.0, window = 'b', mode_f = 0)
    _, full_chirp2 = chirpMod(A_2, ipp, dc_2, sr_tx, sr_rx, fc_2, bw_2, t_d = dc_1*ipp*(1e6/1e2), window = 'r', mode_f = 0)
    full_chirp = np.array(full_chirp1) + np.array(full_chirp2)

    t = [i for i in range(len(full_chirp))] 
    plt.plot(t, np.real(full_chirp))
    plt.plot(t, np.imag(full_chirp))
    plt.show() 

    return full_chirp

generateBlind()