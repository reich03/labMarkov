import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from scipy.stats import spearmanr

# Cargar los datos
datos_loteria = pd.read_csv('clotery.csv', header=None)

# Convertir la columna 'Numero' a numérico
numero = datos_loteria[0]

# Definir números consecutivos y sus sucesores
numeros_consecutivos = numero.iloc[:-1].reset_index(drop=True)
numeros_siguientes = numero.iloc[1:].reset_index(drop=True)

# Calcular la correlación de Spearman
correlacion_spearman, p_valor = spearmanr(numeros_consecutivos, numeros_siguientes)


# Cálculo del estadístico de Chi-cuadrado para evaluar la uniformidad
# Dividimos el rango de 0 a 1000 en bins y contamos las frecuencias en cada bin para aplicar la prueba
bin_counts, _ = np.histogram(numero, bins=10, range=(0,1000))
expected_counts = np.ones_like(bin_counts) * len(numero) / len(bin_counts)  # Esperamos una distribución uniforme

chi_stat, chi_p = chisquare(bin_counts, expected_counts)


chi_stat, chi_p

# Imprimir los resultados de la correlación
print(f"Correlación de Spearman: {correlacion_spearman}, P-valor: {p_valor}, Prueba chi-cuadrado(P-valor:{chi_p}, Chi-statistic:{chi_stat}) \n ")
print("Spearman demuestra independencia estadistica mediante una prueba de correlacion donde un valor minimo de -1 demuestra una tendencia negativa un maximo de 1 una tendencia creciente y cercano o igual a 0 como no correlacion entre las variables, en este caso el dia jugado y el numero caido y chi-cuadrado plantea una hipotesis nula de que los datos de la muestra se distribuyen uniformemente/tienen un comportamiento de distribucion aleatoria, como el p valor asociado al estadistico chi es mayor a 0.05 no hay suficiente evidencia para refutar la hipotesis nula de que los datos se distribuyen uniformemente")


# Gráfico de dispersión para visualizar la relación entre números ganadores consecutivos
plt.figure(figsize=(10, 6))
plt.scatter(numeros_consecutivos, numeros_siguientes, alpha=0.6)
plt.title('Grafico de transiciones de numeros ganadores')
plt.xlabel('Número Ganador en Día N')
plt.ylabel('Número Ganador en Día N+1')
plt.grid(True)
plt.show()

# Crear una secuencia numérica que represente cada sorteo (índice de cada número ganador)
indices_sorteos = np.arange(len(datos_loteria))

# Generar el gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(indices_sorteos, numero, alpha=0.6, color='green')
plt.title('Grafico de numeros ganadores por sorteo')
plt.xlabel('Sorteo No')
plt.ylabel('Número Ganador')
plt.grid(True)
plt.show()