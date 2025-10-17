import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
from datetime import datetime

def iniciar_app():
    añadir_numero()
    inicializar_ventana_principal()

def añadir_numero():
  while True:  # Bucle infinito hasta que el número sea válido
    num_nuevo = simpledialog.askstring("Número Ganador", "Ingrese el número ganador más reciente (debe ser un número de 3 dígitos):")

    if num_nuevo is None:
        sys.exit()  # Detiene la ejecución del programa completamente
    
    if num_nuevo and num_nuevo.isdigit() and 0 <= int(num_nuevo) < 1000:
        # Separar el número en sus dígitos individuales
        num1, num2, num3 = int(num_nuevo[0]), int(num_nuevo[1]), int(num_nuevo[2])
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        new_row = pd.DataFrame([[fecha_actual, num1, num2, num3]], columns=['Fecha', 'Primer', 'Segundo', 'Tercero'])

        try:
            df = pd.read_csv('loteria.csv', delimiter=';')
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv('loteria.csv', sep=';', index=False)
        except FileNotFoundError:
            new_row.to_csv('loteria.csv', sep=';', index=False)
         
        break  # Salir del bucle si el número es válido
    else:
        messagebox.showerror("Error", "Por favor, ingrese un número válido de 3 dígitos.")


def solicitar_n_dias():
    dias = simpledialog.askinteger("Número de días", "Ingrese el número de días para consultar las probabilidades:", minvalue=1, maxvalue=365)
    if dias is None:  # Si el usuario cancela o cierra el diálogo no se consulta el dia
        return
    return dias

def calcular_matrices_transicion():
    df = pd.read_csv('loteria.csv', header=None,sep=';',skiprows=1)
    matriz_transicion = [np.zeros((10, 10)),np.zeros((10, 10)),np.zeros((10, 10))]
    print(len(df[1]))
    for j in range (0,3):
        for i in range(len(df[j+1]) - 1):
         actual= df[j+1][i].astype(int)
         siguiente = df[j+1][i + 1].astype(int)
         matriz_transicion[j][actual][siguiente] += 1

   
    # Normalizar matrices para que cada fila sume exactamente 1.0
    for j in range (0,3):
        for i in range(10):
            total_transiciones = sum(matriz_transicion[j][i])  
            if total_transiciones != 0: 
               # Normalizar cada elemento por la suma total
               for k in range(10):
                   matriz_transicion[j][i][k] = matriz_transicion[j][i][k] / total_transiciones
            else:
               # Si no hay transiciones, asignar probabilidad uniforme
               for k in range(10):
                   matriz_transicion[j][i][k] = 0.1
        
    matrices_trans=[matriz_transicion[0].T,matriz_transicion[1].T,matriz_transicion[2].T]

    
    nombres = [str(i) for i in range(10)]
    
    for i in range(0,3):
        # Guardar en CSV
        pd.DataFrame(matrices_trans[i], index=nombres, columns=nombres).to_csv(f'matriz_transicion_T{i}.csv', index_label='Estado/Numero')
        
        # Imprimir por consola para el profesor
        print(f"\n=== MATRIZ DE TRANSICIÓN - POSICIÓN {i+1} ===")
        print("Estados:  ", end="")
        for j in range(10):
            print(f"{j:8}", end="")
        print()
        
        for fila in range(10):
            print(f"Estado {fila}: ", end="")
            for col in range(10):
                print(f"{matrices_trans[i][fila][col]:7.4f}", end=" ")
            print()
        print("-" * 80)

    numeros=[df[1][len(df[1])-1],df[2][len(df[2])-1],df[3][len(df[3])-1]]

    return numeros, matrices_trans
    

def calcular_probabilidades(dias):
    cond_inicial, matriz_transicion_transpuesta = calcular_matrices_transicion()
  
  
    cond_inicial_vec = [np.zeros(10),np.zeros(10),np.zeros(10)]
    for i in range (0,3):
        if 0 <= cond_inicial[i] < 10:  
         cond_inicial_vec[i][cond_inicial[i].astype(int)] = 1

    
    resultado = [cond_inicial_vec[0].reshape(-1, 1),cond_inicial_vec[1].reshape(-1, 1),cond_inicial_vec[2].reshape(-1, 1)]
    for i in range (0,3):
        pd.DataFrame(resultado[i]).to_csv(f'vector_condicion_inicial{i}.csv')

    for i in range (0,3):
     for _ in range(dias):
            
            resultado[i] = np.dot(matriz_transicion_transpuesta[i], resultado[i])

    return resultado

def mostrar_numero_mas_probable():
    n_dias = solicitar_n_dias()
    resultado = calcular_probabilidades(n_dias)
    if resultado is not None:
        proximo_numero_probable(resultado,n_dias)

def proximo_numero_probable(resultado, n_dias):
    flatres=[[],[],[]]
    maxnum=1
    index=[[],[],[]]
    for i in range(len(resultado)):
        flatres[i]=[elem[0] for elem in resultado[i]]
        maxnum*=max(flatres[i])
        index[i]=flatres[i].index(max(flatres[i]))
        
    messagebox.showinfo("Probabilidad", f"El mumero mas probable para dentro de {n_dias} es el {index[0]}{index[1]}{index[2]} con un {maxnum*100}%")

    
def consultar_probabilidad():
    dias = solicitar_n_dias() 
    if dias is None:  
        return
    
    resultado = calcular_probabilidades(dias)
    if resultado is not None:
        num_input = simpledialog.askstring("Consulta", "Digita el número del que quieras saber la probabilidad de ganar:")
        if num_input is None: 
            messagebox.showerror("Error", "Calculo cancelado o input vacío")
            return
        elif 0 <= int(num_input) < 1000:
            # Completar con ceros a la izquierda para tener siempre 3 dígitos
            num_str = str(int(num_input)).zfill(3)
            prob1 = resultado[0][int(num_str[0])]
            prob2 = resultado[1][int(num_str[1])]
            prob3 = resultado[2][int(num_str[2])]
            probf=prob1*prob2*prob3
            messagebox.showinfo("Probabilidad", f"La probabilidad de que el número {num_input} caiga dentro de {dias} dias es de {100*probf[0]:.4f}%")
        else:
            messagebox.showerror("Error", "Número inválido (debe estar entre 0 y 999)")

def calcular_estado_estable():
    """
    Calcula la distribución estacionaria (estado estable) de las cadenas de Markov
    Usando el método de potencias de matriz o eigenvalores
    """
    try:
        # Cargar matrices de transición
        matriz_T0 = pd.read_csv('matriz_transicion_T0.csv', index_col='Estado/Numero').values
        matriz_T1 = pd.read_csv('matriz_transicion_T1.csv', index_col='Estado/Numero').values
        matriz_T2 = pd.read_csv('matriz_transicion_T2.csv', index_col='Estado/Numero').values
        
        matrices = [matriz_T0, matriz_T1, matriz_T2]
        nombres_posicion = ["Primera", "Segunda", "Tercera"]
        estados_estables = []
        
        resultado_texto = "🎯 DISTRIBUCIONES ESTACIONARIAS (ESTADOS ESTABLES)\n"
        resultado_texto += "=" * 60 + "\n\n"
        
        for i, matriz in enumerate(matrices):
            resultado_texto += f"📊 {nombres_posicion[i]} Posición:\n"
            
            # Método 1: Potencias de matriz (simulando muchos pasos)
            vector_inicial = np.ones(10) / 10  # Distribución uniforme inicial
            matriz_transpuesta = matriz.T
            
            # Iterar muchas veces hasta convergencia
            for paso in range(1000):
                vector_nuevo = np.dot(matriz_transpuesta, vector_inicial)
                # Verificar convergencia
                if np.allclose(vector_inicial, vector_nuevo, atol=1e-8):
                    break
                vector_inicial = vector_nuevo
            
            estados_estables.append(vector_inicial)
            
            # Mostrar resultados
            for digito in range(10):
                probabilidad = vector_inicial[digito]
                resultado_texto += f"  Dígito {digito}: {probabilidad:.6f} ({probabilidad*100:.4f}%)\n"
            
            # Encontrar el dígito más probable
            digito_mas_probable = np.argmax(vector_inicial)
            max_probabilidad = vector_inicial[digito_mas_probable]
            resultado_texto += f"  🎯 Más probable: Dígito {digito_mas_probable} ({max_probabilidad*100:.4f}%)\n"
            resultado_texto += f"  📈 Convergió en {paso+1} iteraciones\n\n"
        
        # Calcular número más probable en estado estable
        numero_mas_probable = ""
        probabilidad_total = 1.0
        
        for i in range(3):
            digito_mas_probable = np.argmax(estados_estables[i])
            numero_mas_probable += str(digito_mas_probable)
            probabilidad_total *= estados_estables[i][digito_mas_probable]
        
        resultado_texto += f"🏆 NÚMERO MÁS PROBABLE EN ESTADO ESTABLE: {numero_mas_probable}\n"
        resultado_texto += f"📊 Probabilidad combinada: {probabilidad_total*100:.6f}%\n\n"
        
        resultado_texto += "💡 INTERPRETACIÓN:\n"
        resultado_texto += "• El estado estable representa las probabilidades límite\n"
        resultado_texto += "• Después de muchos sorteos, estas serían las frecuencias esperadas\n"
        resultado_texto += "• Es independiente del estado inicial\n"
        
        messagebox.showinfo("Estado Estable", resultado_texto)
        print(resultado_texto)  # También imprimir en consola
        
        return estados_estables
        
    except FileNotFoundError:
        messagebox.showerror("Error", "Primero debe calcular las matrices de transición.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular estado estable: {str(e)}")
        return None

def consultar_probabilidad_posicion():
   
    matriz_transicion_transpuesta=[[],[],[]]
    matriz_transicion_transpuesta[0] = pd.read_csv('matriz_transicion_T0.csv', index_col='Estado/Numero').values
    matriz_transicion_transpuesta[1]= pd.read_csv('matriz_transicion_T1.csv', index_col='Estado/Numero').values
    matriz_transicion_transpuesta[2] = pd.read_csv('matriz_transicion_T2.csv', index_col='Estado/Numero').values
    
    posicion = simpledialog.askstring("Consultar Posición", "Ingrese la posición en formato fila,columna (ej. 3,5):")
    if posicion:
        try:
            fila, columna = map(int, posicion.split(","))
            if 0 <= fila < 1000 and 0 <= columna < 1000:
                probabilidad=1
                # Completar con ceros a la izquierda para tener siempre 3 dígitos
                fila_str = str(fila).zfill(3)
                columna_str = str(columna).zfill(3)
                filar=[fila_str[0], fila_str[1], fila_str[2]]
                columnar=[columna_str[0], columna_str[1], columna_str[2]]
                for i in range (0,3,1):
                    probabilidad *= matriz_transicion_transpuesta[i][int(filar[i])][int(columnar[i])]
                # Accede a la probabilidad usando la posición ingresada
                
                messagebox.showinfo("Probabilidad", f"La probabilidad en la posición {fila},{columna} es de {probabilidad} ({100*probabilidad:.4f}%)")
            else:
                messagebox.showerror("Error", "La posición está fuera de rango. Asegúrese de que tanto la fila como la columna estén entre 0 y 999.")
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto. Por favor, ingrese la posición en formato fila,columna (ej. 3,5).")
    else:
        messagebox.showwarning("Cancelado", "Consulta cancelada.")

def inicializar_ventana_principal():
    global ventana, probabilidad_texto, boton_consultar, boton_mas_probable
    ventana = tk.Tk()
    ventana.title("Lotería")
    ventana.geometry("500x300")

    label_menu = tk.Label(ventana, text="Menú", font=("Arial", 16, "bold"))
    label_menu.pack(pady=(10, 0)) 

    label_descripcion = tk.Label(ventana, text="Seleccione una opción para calcular probabilidades o consultarlas.", font=("Arial", 11))
    label_descripcion.pack(pady=(10, 20)) 

    boton_consultar = tk.Button(ventana, font=('Arial', 10) ,text="1. Consultar Probabilidad", command=consultar_probabilidad)
    boton_consultar.pack(pady=10)

    boton_mas_probable = tk.Button(ventana, font=('Arial', 10) ,text="2. Números más Probables", command=mostrar_numero_mas_probable)
    boton_mas_probable.pack(pady=10)

    boton_consultar_posicion = tk.Button(ventana, font=('Arial', 10), text="3. Consultar Posición en Matriz", command=consultar_probabilidad_posicion)
    boton_consultar_posicion.pack(pady=10)

    boton_estado_estable = tk.Button(ventana, font=('Arial', 10), text="4. Estado Estable (Distribución Estacionaria)", command=calcular_estado_estable)
    boton_estado_estable.pack(pady=10)

    probabilidad_texto = tk.StringVar()
    probabilidad_texto.set("")

    label_probabilidad = tk.Label(ventana, textvariable=probabilidad_texto)
    label_probabilidad.pack(pady=10)

    ventana.mainloop()

# Inicia la aplicación con la función que maneja el diálogo inicial
iniciar_app()