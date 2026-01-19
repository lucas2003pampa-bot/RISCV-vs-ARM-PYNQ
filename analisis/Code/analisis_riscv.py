import matplotlib.pyplot as plt
import numpy as np

# --- 1. DATOS REALES (Extraídos de tus capturas) ---
tests = ['Cálculo PI (FPU)', 'Matrices (Mem)', 'Primos (ALU)']

# Tiempos en segundos [ARM, RISC-V]
# Datos sacados de las imágenes:
# PI: ARM=0.000176, RISCV=0.494681
# Matrices: ARM=0.000176, RISCV=0.021115
# Primos: ARM=0.001528, RISCV=0.212268
t_arm = np.array([0.000176, 0.000176, 0.001528])
t_riscv = np.array([0.494681, 0.021115, 0.212268])

# Frecuencias de trabajo (Ajusta si tus valores son distintos)
f_arm = 667e6   # 667 MHz (Zynq-7000 standard)
f_riscv = 50e6  # 50 MHz (Configuración típica PicoRV32)

# --- 2. CÁLCULOS DE INGENIERÍA ---

# A) Speedup Bruto (Cuántas veces más rápido es el ARM)
speedup = t_riscv / t_arm

# B) Ciclos Totales Gastados (Tiempo * Frecuencia)
# Esto elimina la variable del "reloj" y nos deja ver la eficiencia pura del código/arquitectura
cycles_arm = t_arm * f_arm
cycles_riscv = t_riscv * f_riscv

# C) "Lag Arquitectónico" (Efficiency Gap)
# Si el RISC-V fuera a 667MHz, ¿cuántas veces más lento seguiría siendo?
# Esto aísla la falta de Caché/FPU/ALU.
arch_lag = cycles_riscv / cycles_arm

# --- 3. GENERACIÓN DE GRÁFICAS ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
plt.style.use('seaborn-v0_8-whitegrid') # Estilo limpio académico

# GRÁFICA 1: Tiempos de Ejecución (Escala Logarítmica)
x = np.arange(len(tests))
width = 0.35

rects1 = ax1.bar(x - width/2, t_arm, width, label='ARM Cortex-A9', color='#2E86C1')
rects2 = ax1.bar(x + width/2, t_riscv, width, label='RISC-V PicoRV32', color='#E67E22')

ax1.set_ylabel('Tiempo (segundos) - Escala Log')
ax1.set_title('Comparativa de Tiempos (Menos es mejor)')
ax1.set_xticks(x)
ax1.set_xticklabels(tests)
ax1.legend()
ax1.set_yscale('log') # CRÍTICO: Usamos log porque la diferencia en PI es gigante

# GRÁFICA 2: Speedup (El dominio del ARM)
colors_speedup = ['#E74C3C', '#F1C40F', '#2ECC71'] # Rojo para PI (extremo), Verde para normal
bars = ax2.bar(tests, speedup, color=colors_speedup)
ax2.set_ylabel('Speedup (Veces más rápido)')
ax2.set_title('Dominio del ARM (Speedup Bruto)')
ax2.bar_label(bars, fmt='%.0fx', padding=3) # Etiquetas encima de las barras

# GRÁFICA 3: Análisis de Ciclos (La Verdad Arquitectónica)
# Comparamos cuántos ciclos de reloj cuesta hacer la tarea
x = np.arange(len(tests))
ax3.bar(x - width/2, cycles_arm, width, label='Ciclos ARM', color='#5D6D7E')
ax3.bar(x + width/2, cycles_riscv, width, label='Ciclos RISC-V', color='#D35400')

ax3.set_ylabel('Ciclos de Reloj Totales')
ax3.set_title('Ineficiencia de Ciclos (Hardware vs Software)')
ax3.set_xticks(x)
ax3.set_xticklabels(tests)
ax3.set_yscale('log')
ax3.legend()

# Texto explicativo abajo
plt.figtext(0.5, -0.05,
            f"Análisis: Incluso normalizando la frecuencia, el RISC-V necesita {arch_lag[0]:.0f}x más ciclos para PI debido a la falta de FPU.",
            ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})

plt.tight_layout()
plt.show()

# --- 4. IMPRIMIR DATOS PARA TU INFORME ---
print("=== RESULTADOS DEL ANÁLISIS ===")
print(f"{'TEST':<15} | {'ARM (s)':<10} | {'RISC-V (s)':<10} | {'SPEEDUP':<10} | {'LAG ARQUITECTÓNICO'}")
print("-" * 75)
for i in range(len(tests)):
    print(f"{tests[i]:<15} | {t_arm[i]:<10.6f} | {t_riscv[i]:<10.6f} | {speedup[i]:<9.1f}x | {arch_lag[i]:.1f}x más ciclos")
