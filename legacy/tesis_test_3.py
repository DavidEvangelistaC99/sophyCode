import tesis 
import numpy as np

#------------------------Test N2: Atenuacion de rango ciego-------------------------#
#------------------------------Minimo rango detectable------------------------------#

data_cc = np.load("/home/david/Documents/DATA/results/data_cc_short_pulse.npz")
data_chirp = np.load("/home/david/Documents/DATA/results/data_chirp_short_pulse.npz")

arr_cc = data_cc["data"]
arr_chirp = data_chirp["data"]

# Filtro de umbral SNR (mask = 0.35)
arr_cc_filt = tesis.filter_snr(arr_cc, umbral=0.25)
arr_chirp_filt  = tesis.filter_snr(arr_chirp, umbral=0.25)

# Ajuste de angulos (360)
angles_cc = tesis.interpolate_angles(arr_cc_filt, n_angles=360) 
angles_chirp = tesis.interpolate_angles(arr_chirp_filt, n_angles=360) 

tesis.comparar_nan_range(angles_cc, angles_chirp, rango_max=1, nombre_salida="/home/david/Documents/DATA/results/compare_test_2__.csv")

# Impresion de valores maximos y minimos de cada senal por canal
print("CC 0.5%")
tesis.print_min_max_snr(10.0*np.log10(angles_cc))
print("Chirp 0.5%")
tesis.print_min_max_snr(10.0*np.log10(angles_chirp))

tesis.plot_compare_polar_dB(angles_cc, angles_chirp, labels=('SNR CC 0.5%', 'SNR Chirp 0.5%'), max_range_km=1, channel=0, cmap='jet', mode='side')