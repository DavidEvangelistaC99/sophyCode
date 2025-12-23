import numpy as np
import matplotlib.pyplot as plt

def sinGen (amp, ipp, dc, sr):

    n = int(ipp*sr)
    nO = int(dc*n/100.0)

    ones = np.ones(nO)
    zeros = np.zeros(int(n-nO))

    test = amp*np.concatenate((ones,zeros))

    return test

