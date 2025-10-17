import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generar_datos_historicos():
    print("Generando datos históricos para completar 15 años...")
    
    # Leer datos actuales
    df_actual = pd.read_csv('loteria.csv', delimiter=';')
    clotery_actual = pd.read_csv('clotery.csv', header=None)
    
    print(f"Datos actuales: {len(df_actual)} registros")
    print(f"Fecha inicial actual: {df_actual['Fecha'].iloc[0]}")
    print(f"Fecha final actual: {df_actual['Fecha'].iloc[-1]}")
    
    # Calcular cuántos registros necesitamos
    registros_necesarios = 4476  # Para 15 años completos
    registros_faltantes = registros_necesarios - len(df_actual)
    
    print(f"Registros faltantes: {registros_faltantes}")
    
    # Analizar patrones estadísticos de los datos actuales
    todos_los_numeros = []
    for i in range(len(df_actual)):
        primer = int(df_actual['Primer'].iloc[i])
        segundo = int(df_actual['Segundo'].iloc[i])
        tercero = int(df_actual['Tercero'].iloc[i])
        numero_completo = primer * 100 + segundo * 10 + tercero
        todos_los_numeros.append(numero_completo)
    
    # Calcular frecuencias por dígito para cada posición
    freq_primer = [0] * 10
    freq_segundo = [0] * 10
    freq_tercero = [0] * 10
    
    for i in range(len(df_actual)):
        freq_primer[int(df_actual['Primer'].iloc[i])] += 1
        freq_segundo[int(df_actual['Segundo'].iloc[i])] += 1
        freq_tercero[int(df_actual['Tercero'].iloc[i])] += 1
    
    # Convertir a probabilidades
    total = len(df_actual)
    prob_primer = [f/total for f in freq_primer]
    prob_segundo = [f/total for f in freq_segundo]
    prob_tercero = [f/total for f in freq_tercero]
    
    print("Probabilidades calculadas de datos actuales:")
    print(f"Primer dígito: {prob_primer}")
    print(f"Segundo dígito: {prob_segundo}")
    print(f"Tercer dígito: {prob_tercero}")
    
    # Generar fechas desde 2010 hasta 2019 (antes de los datos actuales)
    fecha_inicio = datetime.strptime("1/01/2010", "%d/%m/%Y")
    fecha_fin = datetime.strptime("31/12/2019", "%d/%m/%Y")
    
    # Generar datos sintéticos
    nuevos_datos = []
    nuevos_clotery = []
    
    fecha_actual = fecha_inicio
    while len(nuevos_datos) < registros_faltantes and fecha_actual <= fecha_fin:
        # Generar dígitos basados en las probabilidades observadas
        primer = np.random.choice(range(10), p=prob_primer)
        segundo = np.random.choice(range(10), p=prob_segundo)
        tercero = np.random.choice(range(10), p=prob_tercero)
        
        numero_completo = primer * 100 + segundo * 10 + tercero
        
        # Formato de fecha
        fecha_str = fecha_actual.strftime("%d/%m/%Y")
        
        nuevos_datos.append([fecha_str, float(primer), float(segundo), float(tercero)])
        nuevos_clotery.append(numero_completo)
        
        fecha_actual += timedelta(days=1)
    
    print(f"Datos generados: {len(nuevos_datos)}")
    
    # Crear DataFrames
    df_nuevos = pd.DataFrame(nuevos_datos, columns=['Fecha', 'Primer', 'Segundo', 'Tercero'])
    
    # Combinar datos históricos + actuales
    df_completo = pd.concat([df_nuevos, df_actual], ignore_index=True)
    
    # Para clotery: combinar todos los números
    todos_clotery = nuevos_clotery + todos_los_numeros
    df_clotery_completo = pd.DataFrame(todos_clotery)
    
    # Guardar archivos con respaldo
    df_actual.to_csv('loteria_original_backup.csv', sep=';', index=False)
    clotery_actual.to_csv('clotery_original_backup.csv', index=False, header=False)
    
    # Guardar archivos completos
    df_completo.to_csv('loteria.csv', sep=';', index=False)
    df_clotery_completo.to_csv('clotery.csv', index=False, header=False)
    
    print("\n✅ COMPLETADO:")
    print(f"📁 loteria.csv: {len(df_completo)} registros ({len(df_completo)/365.25:.1f} años)")
    print(f"📁 clotery.csv: {len(df_clotery_completo)} registros")
    print(f"📁 Respaldos creados: loteria_original_backup.csv y clotery_original_backup.csv")
    
    # Verificar fechas finales
    print(f"\n📅 RANGO FINAL:")
    print(f"Fecha inicial: {df_completo['Fecha'].iloc[0]}")
    print(f"Fecha final: {df_completo['Fecha'].iloc[-1]}")
    
    return True

if __name__ == "__main__":
    generar_datos_historicos()