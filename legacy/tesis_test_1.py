import tesis 
import numpy as np


#--------------------------Test N1: Aumento de sensiblidad--------------------------#
#---------------------------------Comparacion de SNR--------------------------------#

data_12_1 = np.load("/home/david/Documents/DATA/results/data_chirp_large_pulse.npz")
data_cc = np.load("/home/david/Documents/DATA/results/data_cc_large_pulse.npz")

arr_12_1 = data_12_1["data"]
arr_cc = data_cc["data"]

# Filtro de umbral SNR (mask = 0.35)
arr_12_1_filt = tesis.filter_snr(arr_12_1, umbral=0.35)
arr_cc_filt  = tesis.filter_snr(arr_cc, umbral=0.35)

# Ajuste de angulos (360)
angles_12_1 = tesis.interpolate_angles(arr_12_1_filt, n_angles=360) 
angles_cc = tesis.interpolate_angles(arr_cc_filt, n_angles=360) 

# Remover parte central (potencia de TX)
DC_1 = 14.5
DC_2 = 14.5
angles_12_1 = tesis.apply_duty_cycle_mask(angles_12_1, duty_cycle=DC_1, max_range_km=60.0)
angles_cc = tesis.apply_duty_cycle_mask(angles_cc, duty_cycle=DC_1, max_range_km=60.0)

# Promedio de SNR por angulo
data_avg_12_1 = tesis.mean_dB_valid(angles_12_1, N=0)
data_avg_cc = tesis.mean_dB_valid(angles_cc, N=0)

print(data_avg_12_1.shape)

# Comparacion de SNR promedio por angulo entre las dos senales
tesis.compare_snr(data_avg_12_1, data_avg_cc, "/home/david/Documents/DATA/results/compare_snr_test_1____.csv")

# Impresion de valores maximos y minimos de cada senal por canal
print("CC")
tesis.print_min_max_snr(10.0*np.log10(angles_cc))
print("Chirp")
tesis.print_min_max_snr(10.0*np.log10(angles_12_1))

# Graficas de visualizacion del SNR
tesis.plot_compare_polar_dB(angles_cc, angles_12_1, labels=('SNR CC', 'SNR Chirp'), max_range_km=60, channel=0, cmap='jet', mode='side')


