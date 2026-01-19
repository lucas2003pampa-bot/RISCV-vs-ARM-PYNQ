# Análisis: Validación de Rendimiento RISC-V vs ARM

Este directorio contiene las herramientas de ciencia de datos y los scripts de post-procesado desarrollados para cuantificar y visualizar la diferencia de rendimiento entre el núcleo sintetizado (PicoRV32) y el procesador físico (ARM Cortex-A9).

## Contenido del Directorio

El módulo de análisis se divide en dos secciones principales para separar el código de los resultados visuales:

* **`code/` (Procesamiento):** Contiene los scripts de Python encargados de la ingesta de datos brutos, el cálculo de métricas (Speedup) y la generación de gráficas.
    * `analisis_riscv.py`: Script principal que automatiza la creación de las gráficas comparativas.
* **`graficas/` (Visualización):** Almacena los resultados gráficos generados, evidenciando el impacto de la arquitectura en los tiempos de ejecución.
    * Incluye las comparativas en **escala logarítmica**, necesarias debido a la diferencia de magnitud entre ambas arquitecturas.

## Estructura del Análisis

El flujo de trabajo implementado en este directorio sigue una metodología de validación cruzada con el hardware:

1. **Ingesta de Datos:** El script toma los tiempos de ejecución obtenidos en la suite de Software (Matrix Multiplication, Primes, PI).
2. **Normalización y Escala:** Debido a la naturaleza del núcleo PicoRV32 configurado (RV32I sin multiplicador hardware), los tiempos difieren en órdenes de magnitud (x100 - x600). Se aplican transformaciones logarítmicas para una visualización correcta.
3. **Generación de Evidencias:** Se exportan las imágenes finales que confirman las limitaciones de la arquitectura *soft-core* frente al *hard-core*.

## Requisitos

Para replicar el análisis y regenerar las gráficas se requiere:

* **Lenguaje:** Python 3.x.
* **Librerías:** `pandas` (manejo de datos), `matplotlib` y `seaborn` (visualización).

## Interpretación de Resultados

El objetivo de este módulo no es solo graficar, sino **validar el diseño hardware** mediante datos:

* Los scripts confirman que la **ausencia de unidades DSP (Multiplicación/División)** en el bitstream del PicoRV32 obliga a una emulación por software, resultando en el "Speedup" masivo a favor del ARM observado en las gráficas.
* Se correlaciona el bajo consumo de recursos (LUTs) reportado en Vivado con el menor rendimiento obtenido, validando el diseño como una solución orientada a control y no a cómputo intensivo.
