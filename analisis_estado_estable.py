import pandas as pd
import numpy as np
from scipy.linalg import eig

def analizar_estado_estable_detallado():
    """
    Análisis matemático completo del estado estable usando diferentes métodos
    """
    print("🔬 ANÁLISIS MATEMÁTICO DETALLADO DEL ESTADO ESTABLE")
    print("=" * 70)
    
    try:
        # Cargar matrices
        matriz_T0 = pd.read_csv('matriz_transicion_T0.csv', index_col='Estado/Numero').values
        matriz_T1 = pd.read_csv('matriz_transicion_T1.csv', index_col='Estado/Numero').values
        matriz_T2 = pd.read_csv('matriz_transicion_T2.csv', index_col='Estado/Numero').values
        
        matrices = [matriz_T0, matriz_T1, matriz_T2]
        nombres = ["Primera Posición", "Segunda Posición", "Tercera Posición"]
        
        for i, (matriz, nombre) in enumerate(zip(matrices, nombres)):
            print(f"\n📊 {nombre}")
            print("-" * 50)
            
            # MÉTODO 1: Eigenvalores y eigenvectores
            print("🔹 Método 1: Eigenvalores")
            eigenvalores, eigenvectores = eig(matriz.T)
            
            # Encontrar el eigenvalor 1 (o el más cercano a 1)
            idx_estacionario = np.argmin(np.abs(eigenvalores - 1))
            eigenvector_estacionario = np.real(eigenvectores[:, idx_estacionario])
            
            # Normalizar para que sume 1
            if np.sum(eigenvector_estacionario) != 0:
                estado_estable_eigen = eigenvector_estacionario / np.sum(eigenvector_estacionario)
                estado_estable_eigen = np.abs(estado_estable_eigen)  # Asegurar valores positivos
            else:
                estado_estable_eigen = np.ones(10) / 10
            
            print(f"Eigenvalor dominante: {eigenvalores[idx_estacionario]:.8f}")
            
            # MÉTODO 2: Potencias de matriz
            print("🔹 Método 2: Potencias de Matriz")
            vector_inicial = np.ones(10) / 10
            matriz_T = matriz.T
            
            for iteracion in range(1000):
                vector_nuevo = np.dot(matriz_T, vector_inicial)
                if np.allclose(vector_inicial, vector_nuevo, atol=1e-10):
                    break
                vector_inicial = vector_nuevo
            
            estado_estable_potencias = vector_inicial
            print(f"Convergencia en: {iteracion+1} iteraciones")
            
            # MÉTODO 3: Sistema de ecuaciones π = πP
            print("🔹 Método 3: Sistema de Ecuaciones")
            A = matriz.T - np.eye(10)
            A = np.vstack([A, np.ones(10)])  # Agregar restricción de suma = 1
            b = np.zeros(11)
            b[-1] = 1
            
            # Resolver usando mínimos cuadrados
            estado_estable_sistema, residuos, rank, s = np.linalg.lstsq(A, b, rcond=None)
            
            # Comparar métodos
            print("\n📈 Comparación de Métodos:")
            print("Dígito | Eigenval.  | Potencias  | Sistema    | Diferencia")
            print("-" * 55)
            
            max_diferencia = 0
            for j in range(10):
                diff = abs(estado_estable_eigen[j] - estado_estable_potencias[j])
                max_diferencia = max(max_diferencia, diff)
                print(f"  {j}    | {estado_estable_eigen[j]:.8f} | {estado_estable_potencias[j]:.8f} | {estado_estable_sistema[j]:.8f} | {diff:.2e}")
            
            print(f"\nMáxima diferencia entre métodos: {max_diferencia:.2e}")
            
            if max_diferencia < 1e-6:
                print("✅ EXCELENTE: Todos los métodos convergen al mismo resultado")
            elif max_diferencia < 1e-4:
                print("✅ BUENO: Los métodos son consistentes")
            else:
                print("⚠️  ADVERTENCIA: Hay diferencias significativas entre métodos")
            
            # Análisis de propiedades
            print(f"\n🔍 Propiedades del Estado Estable:")
            print(f"• Suma total: {np.sum(estado_estable_potencias):.10f}")
            print(f"• Dígito más probable: {np.argmax(estado_estable_potencias)} ({np.max(estado_estable_potencias)*100:.4f}%)")
            print(f"• Dígito menos probable: {np.argmin(estado_estable_potencias)} ({np.min(estado_estable_potencias)*100:.4f}%)")
            print(f"• Entropía: {-np.sum(estado_estable_potencias * np.log2(estado_estable_potencias + 1e-10)):.6f} bits")
            
            # Verificar propiedad estacionaria π = πP
            verificacion = np.dot(estado_estable_potencias, matriz)
            error_estacionario = np.linalg.norm(verificacion - estado_estable_potencias)
            print(f"• Error estacionario ||π - πP||: {error_estacionario:.2e}")
            
            if error_estacionario < 1e-8:
                print("✅ VERIFICADO: π = πP (propiedad estacionaria cumplida)")
            else:
                print("⚠️  La propiedad estacionaria tiene error numérico")
        
        print(f"\n🏆 CONCLUSIÓN GENERAL:")
        print("• El estado estable representa el comportamiento a largo plazo")
        print("• Es independiente del estado inicial")
        print("• Indica las frecuencias límite de cada dígito")
        print("• Útil para entender el equilibrio del sistema")
        
    except FileNotFoundError:
        print("❌ Error: Primero ejecute el programa principal para generar las matrices")
    except Exception as e:
        print(f"❌ Error en el análisis: {str(e)}")

if __name__ == "__main__":
    analizar_estado_estable_detallado()