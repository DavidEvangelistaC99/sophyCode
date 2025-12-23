import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d


def filter_snr(data, umbral=0.35):
    """
    Reemplaza los valores menores a 'umbral' por NaN.
    data: arreglo numpy (2, n, m)
    umbral: valor de SNR mínimo permitido
    """
    data_filtrada = np.copy(data)  # evita modificar el arreglo original
    data_filtrada[data_filtrada < umbral] = np.nan

    return data_filtrada

def interpolate_angles(data, n_angles=360):
    """
    Interpola un arreglo (2, n, m) al número deseado de ángulos (por defecto 360).

    Parámetros:
    -----------
    data : np.ndarray
        Arreglo de forma (2, n, m)
    n_angulos_deseados : int
        Número final de ángulos, normalmente 360

    Retorna:
    --------
    data_interp : np.ndarray
        Arreglo interpolado de forma (2, n_angulos_deseados, m)
    """

    # Verificar dimensiones
    if data.ndim != 3 or data.shape[0] != 2:
        raise ValueError("El arreglo debe tener forma (2, n, m)")

    _, n, m = data.shape

    # Ejes originales y nuevos
    angles_old = np.linspace(0, 360, n, endpoint=False)
    angles_new = np.linspace(0, 359, n_angles)
    samples = np.arange(m)

    # Crear nuevo arreglo
    data_interp = np.zeros((2, n_angles, m))

    for ch in range(2):
        f = RegularGridInterpolator(
            (angles_old, samples),
            data[ch],
            method='linear',
            bounds_error=False,
            fill_value=np.nan
        )

        # Crear malla para los nuevos ángulos
        Y, X = np.meshgrid(angles_new, samples, indexing='ij')
        pts = np.array([Y.ravel(), X.ravel()]).T

        data_interp[ch] = f(pts).reshape(n_angles, m)

    return data_interp


def apply_duty_cycle_mask(data, duty_cycle=10, max_range_km=60.0):
    """
    Aplica una máscara (NaN) a los primeros bins de cada ángulo según el duty cycle.
    
    Parámetros:
    -----------
    data : np.ndarray
        Arreglo de forma (2, 360, m)
    duty_cycle : float
        Porcentaje de duty cycle (por ejemplo, 10 para 10%)
    max_range_km : float
        Alcance máximo total (por defecto 60 km)
    
    Retorna:
    --------
    data_masked : np.ndarray
        Copia del arreglo original con los primeros bins de cada ángulo puestos en NaN,
        equivalentes al duty cycle definido.
    """
    if data.ndim != 3 or data.shape[0] != 2 or data.shape[1] != 360:
        raise ValueError("El arreglo debe tener forma (2, 360, m)")
    
    data_masked = np.copy(data).astype(float)
    
    # Porcentaje de bins a anular según duty cycle
    _, _, m = data.shape
    frac = duty_cycle / 100.0
    n_mask = int(np.round(frac * m))  # número de bins a hacer NaN

    # Evitar valores fuera de rango
    n_mask = max(0, min(n_mask, m))

    # Aplicar NaN en los primeros n_mask bins
    if n_mask > 0:
        data_masked[:, :, :n_mask] = np.nan

    # Retornar
    return data_masked


def resample_bins(data, new_bins=1000):
    """
    Interpola el eje de rango (bins) para ajustar todos los ángulos
    al mismo número de elementos (new_bins).
    
    data: arreglo (2, n_angles, n_bins)
    new_bins: número deseado de bins por ángulo (ej. 1000)
    """
    channels, n_angles, n_bins = data.shape
    new_data = np.zeros((channels, n_angles, new_bins))
    
    old_x = np.linspace(0, 1, n_bins)
    new_x = np.linspace(0, 1, new_bins)
    
    for ch in range(channels):
        for ang in range(n_angles):
            y = data[ch, ang, :]
            # ignorar NaN en la interpolación
            valid = ~np.isnan(y)
            if np.sum(valid) > 1:
                f = interp1d(old_x[valid], y[valid], kind='linear',
                             fill_value="extrapolate", bounds_error=False)
                new_data[ch, ang, :] = f(new_x)
            else:
                new_data[ch, ang, :] = np.nan
    return new_data


def mean_dB_valid(data, N):
    """
    Calcula el promedio de SNR ignorando los primeros N valores de cada ángulo.
    data: arreglo (2, 360, m)
    N: cantidad de muestras iniciales a ignorar
    
    Retorna:
        data_avg_log: arreglo (2, 360, 1) en escala logarítmica (dB)
    """

    canales, angulos, m = data.shape
    data_avg = np.zeros((canales, angulos, 1))

    for ch in range(canales):
        for ang in range(angulos):
            # Ignoramos los primeros N elementos de cada ángulo
            vals = data[ch, ang, N:]
            
            # Eliminamos NaN para el promedio
            valid = vals[~np.isnan(vals)]
            
            # Promedio solo considerando valores válidos
            if len(valid) > 0:
                mean_val = np.mean(valid)
            else:
                mean_val = np.nan

            data_avg[ch, ang, 0] = mean_val

    # Evitar log10(0) o log10(NaN)
    data_avg[data_avg <= 0] = np.nan

    # Convertimos a escala logarítmica
    data_avg_log = 10 * np.log10(data_avg)

    # Imprimir mínimo y máximo de cada canal
    for ch in range(canales):
        snr_ch = data_avg_log[ch, :, 0]
        snr_min = np.nanmin(snr_ch)
        snr_max = np.nanmax(snr_ch)
        ang_min = np.nanargmin(snr_ch)
        ang_max = np.nanargmax(snr_ch)
        
        print(f"\nCanal {ch+1}:")
        print(f"  SNR mínimo  = {snr_min:.2f} dB  (ángulo {ang_min}°)")
        print(f"  SNR máximo  = {snr_max:.2f} dB  (ángulo {ang_max}°)")

    data_avg_log = np.roll(data_avg_log, shift=-2, axis=1)
    
    return data_avg_log


def mean_dB_DC(data, DC):
    """
    Calcula el promedio de SNR considerando SOLO el porcentaje de bins definido
    por el duty cycle (DC) desde el inicio de cada ángulo.
    Los NaN se reemplazan por 0 para no eliminar bins.

    data: arreglo (2, 360, m)
    DC: duty cycle en porcentaje (%)

    Retorna:
        data_avg_log: arreglo (2, 360, 1) en escala logarítmica (dB)
    """

    canales, angulos, m = data.shape

    # Convertir duty cycle (%) a número de bins
    N = int((DC / 100) * m)
    if N <= 0:
        raise ValueError("El duty cycle es demasiado pequeño, N=0 bins seleccionados.")
    if N > m:
        N = m

    data_avg = np.zeros((canales, angulos, 1))

    for ch in range(canales):
        for ang in range(angulos):
            # Considerar solo los primeros N elementos (según DC)
            vals = data[ch, ang, :N]
            
            # Reemplazar NaN por 0
            vals_no_nan = np.nan_to_num(vals, nan=0.0)
            
            # Promedio considerando SOLO los N bins
            mean_val = np.sum(vals_no_nan) / N
            data_avg[ch, ang, 0] = mean_val

    # Evitar log10(0)
    data_avg[data_avg <= 0] = np.nan

    # Convertir a escala logarítmica (dB)
    data_avg_log = 10 * np.log10(data_avg)

    # Imprimir mínimo y máximo de cada canal
    for ch in range(canales):
        snr_ch = data_avg_log[ch, :, 0]
        snr_min = np.nanmin(snr_ch)
        snr_max = np.nanmax(snr_ch)
        ang_min = np.nanargmin(snr_ch)
        ang_max = np.nanargmax(snr_ch)
        
        print(f"\nCanal {ch+1}:")
        print(f"  Duty cycle = {DC}%  →  {N} bins considerados")
        print(f"  SNR mínimo  = {snr_min:.2f} dB  (ángulo {ang_min}°)")
        print(f"  SNR máximo  = {snr_max:.2f} dB  (ángulo {ang_max}°)")

    return data_avg_log


def compare_snr(snr1, snr2, filename="compare_snr.csv"):
    """
    Crea una comparación entre dos arreglos de SNR de forma (2, 360, 1)
    y guarda los resultados en un archivo CSV separado por espacios.
    
    El archivo contendrá columnas:
      Canal, Ángulo, SNR_1, SNR_2, Diferencia (SNR_1 - SNR_2), Diferencia_noNaN
    """

    canales, angulos, _ = snr1.shape
    resultados = []

    for ch in range(canales):
        for ang in range(angulos):
            val1 = snr1[ch, ang, 0]
            val2 = snr2[ch, ang, 0]

            # Calcular diferencia
            diff = val1 - val2

            # Sustituir NaN por 0 para la nueva columna
            diff_no_nan = 0.0 if np.isnan(diff) else diff

            resultados.append([ch + 1, ang, val1, val2, diff, diff_no_nan])

    # Convertimos a DataFrame
    columnas = ["Canal", "Ángulo", "SNR_1", "SNR_2", "Diferencia", "Diferencia_noNaN"]
    df = pd.DataFrame(resultados, columns=columnas)

    # Imprimir resultados por canal
    for ch in range(canales):
        print(f"\nCanal {ch+1}:")
        print(df[df["Canal"] == ch + 1].to_string(index=False))

    # Guardar en CSV separado por espacios
    df.to_csv(filename, sep=' ', index=False, float_format='%.4f')
    print(f"\nResultados guardados en '{filename}'")

    return df


def print_min_max_snr(data):
    """
    Imprime el valor mínimo y máximo del SNR para cada canal.
    
    Parámetros:
    -----------
    data : np.ndarray
        Arreglo de forma (2, 360, m)
    """

    canales, angulos, m = data.shape
    if canales != 2:
        raise ValueError("El arreglo debe tener dos canales en la primera dimensión (2, 360, m).")
    
    for ch in range(canales):
        data_ch = np.copy(data[ch])
        data_ch[np.isnan(data_ch)] = np.nan  # por si hay NaN
        min_val = np.nanmin(data_ch)
        max_val = np.nanmax(data_ch)
        print(f"Canal {ch+1}: SNR mínimo = {min_val:.3f}, SNR máximo = {max_val:.3f}")


def plot_polar_channel_dB(data, max_range_km=60, channel=0, cmap='jet'):
    """
    Muestra un gráfico circular (polar) del SNR en escala logarítmica (dB)
    para un canal del arreglo de forma (2, 360, m).

    Parámetros:
        data : np.ndarray
            Arreglo de forma (2, 360, m)
        max_range_km : float
            Valor máximo del eje radial (por defecto 60 km)
        channel : int
            Canal a graficar (0 o 1)
        cmap : str
            Mapa de colores para visualizar la intensidad
    """

    canales, angulos, m = data.shape

    if channel >= canales:
        raise ValueError(f"El canal {channel} no existe. El arreglo solo tiene {canales} canales.")
    
    # Reemplazar valores no válidos (<=0 o NaN) antes de aplicar log10
    data_channel = np.copy(data[channel])
    data_channel[data_channel <= 0] = np.nan
    
    # Conversión a escala logarítmica (dB)
    data_db = 10 * np.log10(data_channel)
    
    # Crear ejes: 360 grados → 0 a 2π, rango → 0 a max_range_km
    theta = np.linspace(0, 2 * np.pi, angulos)
    r = np.linspace(0, max_range_km, m)
    
    # Transponer para que r sea el eje vertical
    Z = data_db.T  # Z.shape = (m, 360)
    
    # Crear gráfico polar
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    c = ax.pcolormesh(theta, r, Z, shading='auto', cmap=cmap,
                  vmin=10*np.log10(0.35), vmax=25)
    
    # Configuración estética
    ax.set_title(f"Canal {channel+1} - SNR (dB)", va='bottom', fontsize=13)
    ax.set_theta_zero_location("N")  # 0° arriba
    ax.set_theta_direction(-1)       # Sentido horario
    ax.set_rlabel_position(225)      # Mueve etiquetas del radio
    
    # Barra de color
    cbar = plt.colorbar(c, ax=ax, pad=0.1)
    cbar.set_label('SNR [dB]', rotation=270, labelpad=15)
    
    plt.show()


def plot_compare_polar_dB(data1, data2, labels=('Data 1', 'Data 2'),
                          max_range_km=60, channel=0, cmap='jet',
                          mode='side'):
    """
    Muestra dos gráficos polares comparativos de SNR (en dB) para un canal específico.
    El rango de color (vmin, vmax) se ajusta automáticamente según ambas datasets.

    Parámetros:
    -----------
    data1, data2 : np.ndarray
        Arreglos de forma (2, 360, m1) y (2, 360, m2), respectivamente.
        Cada uno contiene la SNR en escala lineal.
    labels : tuple(str, str)
        Nombres o etiquetas para cada dataset (por ejemplo: ('Chirp', 'Complementario')).
    max_range_km : float
        Alcance máximo radial (por defecto 60 km).
    channel : int
        Canal a graficar (0 o 1).
    cmap : str
        Mapa de colores (por defecto 'jet').
    mode : str
        'side' → muestra ambos mapas lado a lado.
        'overlay' → los superpone con transparencia.
    """

    # --- Validaciones básicas ---
    for data, name in zip((data1, data2), labels):
        if data.ndim != 3 or data.shape[0] != 2:
            raise ValueError(f"{name} debe tener forma (2, 360, m)")
        if channel >= data.shape[0]:
            raise ValueError(f"El canal {channel} no existe en {name}.")

    # --- Conversión de ambos datasets a dB ---
    def to_dB(x):
        x = np.copy(x[channel])
        x[x <= 0] = np.nan
        return 10 * np.log10(x)

    db1 = to_dB(data1)
    db2 = to_dB(data2)

    # --- Cálculo automático de vmin/vmax (ignorando NaN) ---
    combined = np.concatenate([
        db1[np.isfinite(db1)].ravel(),
        db2[np.isfinite(db2)].ravel()
    ])
    vmin, vmax = np.nanmin(combined), np.nanmax(combined)

    # --- Ejes ---
    angulos = 360
    theta = np.linspace(0, 2 * np.pi, angulos)
    r1 = np.linspace(0, max_range_km, db1.shape[1])
    r2 = np.linspace(0, max_range_km, db2.shape[1])

    Z1 = db1.T
    Z2 = db2.T

    # --- Crear figura ---
    if mode == 'side':
        fig, axes = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(14, 7))
        axs = axes
    elif mode == 'overlay':
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
        axs = [ax]
    else:
        raise ValueError("mode debe ser 'side' o 'overlay'")

    # --- Gráfico 1 ---
    c1 = axs[0].pcolormesh(theta, r1, Z1, shading='auto', cmap=cmap, vmin=vmin, vmax=vmax)
    axs[0].set_title(f"{labels[0]}", va='bottom', fontsize=13)
    axs[0].set_theta_zero_location("N")
    axs[0].set_theta_direction(-1)
    axs[0].set_rlabel_position(225)
    plt.colorbar(c1, ax=axs[0], pad=0.1, label='SNR [dB]', shrink=0.7)

    # --- Gráfico 2 ---
    if mode == 'side':
        c2 = axs[1].pcolormesh(theta, r2, Z2, shading='auto', cmap=cmap, vmin=vmin, vmax=vmax)
        axs[1].set_title(f"{labels[1]}", va='bottom', fontsize=13)
        axs[1].set_theta_zero_location("N")
        axs[1].set_theta_direction(-1)
        axs[1].set_rlabel_position(225)
        plt.colorbar(c2, ax=axs[1], pad=0.1, label='SNR [dB]', shrink=0.7)

    elif mode == 'overlay':
        c1 = axs[0].pcolormesh(theta, r1, Z1, shading='auto', cmap='jet', alpha=0.6, vmin=vmin, vmax=vmax)
        c2 = axs[0].pcolormesh(theta, r2, Z2, shading='auto', cmap='inferno', alpha=0.6, vmin=vmin, vmax=vmax)
        axs[0].set_title(f"Comparación - {labels[0]} (azul) vs {labels[1]} (naranja)", fontsize=13)
        axs[0].set_theta_zero_location("N")
        axs[0].set_theta_direction(-1)
        axs[0].set_rlabel_position(225)
        plt.colorbar(c1, ax=axs[0], pad=0.1, label=f'{labels[0]} [dB]', shrink=0.7)
        plt.colorbar(c2, ax=axs[0], pad=0.15, label=f'{labels[1]} [dB]', shrink=0.7)

    plt.tight_layout()
    plt.show()


def comparar_nan_range(arr1, arr2, rango_max=10.0, nombre_salida=""):
    """
    Compara el rango (en km) del primer NaN encontrado por ángulo en dos arreglos.
    Guarda los resultados en un archivo CSV.

    Parámetros:
        arr1, arr2 : np.ndarray
            Arreglos de forma (2, 360, n1) y (2, 360, n2)
        rango_max : float
            Rango máximo en km (por defecto 10 km)
        nombre_salida : str
            Nombre del archivo CSV donde guardar los resultados
    """
    # Validar dimensiones iniciales
    if arr1.shape[:2] != arr2.shape[:2]:
        raise ValueError("Los dos arreglos deben tener el mismo número de canales y ángulos (2, 360).")
    
    canales, angulos = arr1.shape[:2]
    n1, n2 = arr1.shape[2], arr2.shape[2]

    bin_to_km_1 = rango_max / n1
    bin_to_km_2 = rango_max / n2

    # Crear listas para armar DataFrame al final
    datos = []

    for c in range(canales):
        print(f"\n=== Canal {c+1} ===")
        print(f"{'Ángulo':>7} | {'R1 (km)':>10} | {'R2 (km)':>10} | {'Dif (km)':>10}")
        print("-" * 46)

        for a in range(angulos):
            # Buscar primer NaN
            idx1 = np.argmax(np.isnan(arr1[c, a]))
            idx2 = np.argmax(np.isnan(arr2[c, a]))

            # Si no hay NaN, usar todo el rango
            if not np.isnan(arr1[c, a]).any():
                idx1 = n1
            if not np.isnan(arr2[c, a]).any():
                idx2 = n2

            # Convertir a km
            r1 = idx1 * bin_to_km_1
            r2 = idx2 * bin_to_km_2
            diff = r2 - r1

            # Guardar para impresión
            print(f"{a:7d} | {r1:10.3f} | {r2:10.3f} | {diff:10.3f}")

            # Agregar fila al dataset
            datos.append({
                "Canal": c + 1,
                "Ángulo": a,
                "R1_km": r1,
                "R2_km": r2,
                "Diferencia_km": diff
            })

    # Convertir a DataFrame
    df = pd.DataFrame(datos)

    # Guardar en CSV
    df.to_csv(nombre_salida, index=False)
    print(f"\n Resultados guardados en: {nombre_salida}")

    # Retornar también los arrays si se desea seguir procesando
    R1 = df.pivot(index="Ángulo", columns="Canal", values="R1_km").to_numpy().T
    R2 = df.pivot(index="Ángulo", columns="Canal", values="R2_km").to_numpy().T
    Diff = df.pivot(index="Ángulo", columns="Canal", values="Diferencia_km").to_numpy().T

    return R1, R2, Diff

