# Proyecto T08: RISC-V en FPGA PYNQ-Z2
Comparativa de rendimiento entre Soft Core RISC-V y Hard Core ARM Cortex-A9.

## Estructura del Hardware y Resultados

La organización del repositorio está diseñada para facilitar la replicación y validación del diseño:

* **`hardware/`**:
    * **`src/` (Fuentes):** Contiene los códigos fuente en Verilog necesarios para implementar el núcleo RISC-V.
        * `picorv32.v`: El núcleo del procesador.
        * `tb_riscv.v`: El testbench utilizado para la validación funcional previa.
    * **`scripts/` (Reconstrucción):**
        * `Sistema_completo.tcl`: Script de TCL que permite reconstruir el proyecto de Vivado y el Block Design completo automáticamente sin necesidad de configurar los bloques manualmente.
    * **`outputs/` (Exportación):**
        * `Sistema_completo_wrapper.xsa`: Archivo de especificación de hardware exportado.
        * **Uso:** Este archivo es necesario para crear la **Plataforma** en Vitis. Sobre ella se cargarán los archivos `.c` (ubicados en la carpeta `software/`) para ejecutar los tests y benchmarks.

* **`imagenes/` (Evidencias):**
    * Contiene las capturas de pantalla que validan los **resultados del hardware**, incluyendo la simulación del testbench, el diagrama de bloques final y los tests de memoria/GPIO ejecutados en la terminal.


# Software: Suite de Benchmarks RISC-V vs ARM

Este directorio contiene el código fuente desarrollado para comparar el rendimiento entre el procesador Soft-Core RISC-V (PicoRV32) y el Hard-Core ARM Cortex-A9 sobre FPGA.

## Contenido del Directorio

El software se organiza en tres pruebas de estrés específicas:

* **Numeros_Primos/**: Evalúa la ALU y el set de instrucciones (ISA) mediante el cálculo de números primos, estresando la operación de división entera.
* **Producto_decimales/**: Evalúa el rendimiento de coma flotante (FPU) mediante el cálculo numérico de PI (Suma de Riemann).
* **Producto_Matrices/**: Evalúa la jerarquía de memoria y la latencia de acceso (Caché vs RAM) mediante multiplicación de matrices.

## Estructura de las Pruebas

Cada una de las carpetas anteriores sigue la misma estructura interna:

1. **Raíz (Host ARM):** Contiene los archivos .c principales para ejecutar en Xilinx Vitis. Estos programas ejecutan el test en el ARM, cargan el firmware en el RISC-V y cronometran los resultados.
2. **Subcarpeta Conversion_Hexadecimal (Device RISC-V):** Contiene el código fuente bare-metal para RISC-V, el código de arranque y los scripts necesarios para la compilación cruzada y la conversión del binario a formato hexadecimal.

## Requisitos

* **ARM:** Xilinx Vitis IDE.
* **RISC-V:** xPack GNU RISC-V Embedded GCC.

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
