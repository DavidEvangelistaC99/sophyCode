import matplotlib.pyplot as plt
import numpy as np

valores1 = np.array([
    -18.74, -17.75, -16.74, -15.88, -14.90,
    -13.95, -13.06, -12.13, -11.28, -10.47,
    -9.745, -8.838, -8.103
])

valores2 = np.array([
    40.2, 41.1, 42.5, 43.3, 44.2,
    45.1, 46.3, 46.8, 47.6, 48.3,
    49.2, 50.1, 50.9
])

x = np.array([-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0])
y1 = np.array([38.7, 40.1, 41.1, 42.3, 43.3, 44.1, 45.1, 46.3, 47.0, 47.7, 48.5, 49.5, 50.2])
y2 = np.array([-29.0, -27.3, -25.34, -24.27, -23.62, -22.61, -21.34, -19.94, -19.22, -18.44, -17.08, -16.06, -15.8])
diff = valores2-valores1

print(np.mean(diff))

# plt.scatter(x, y1, color='blue', marker='o', label='SSPA')
# plt.plot(x, y1, linestyle='--', color='blue')


### ULTIMA PRUEBA ###
# plt.scatter(x, valores1, color='red', marker='x', label='Punto de prueba')
# plt.plot(x, valores1, linestyle='--', color='red')

# plt.scatter(x, valores2, color='green', marker='*', label='Interfaz web')
# plt.plot(x, valores2, linestyle='--', color='green')

plt.scatter(x, diff, color='green', marker='*', label='Atenuación SSPA')
plt.plot(x, diff, linestyle='--', color='green')

plt.title('Atenuación Test Point (dBm)')
plt.xlabel('Atenuación (dB)')
plt.grid(True)
plt.legend()
plt.xlim(-13, 1) 
# plt.ylim(-40, 60)
plt.ylim(40, 70)
plt.show()
