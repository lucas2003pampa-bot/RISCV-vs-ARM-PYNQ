# Software

## Benchmarks de Rendimiento y Flujo de Inyección de Firmware RISC-V

Este repositorio contiene la suite de pruebas de rendimiento diseñada para realizar una comparativa técnica exhaustiva entre la arquitectura Soft-Core RISC-V (PicoRV32) y un procesador Hard-Core ARM Cortex-A9 sobre FPGA. El proyecto abarca desde los algoritmos de prueba de alto nivel hasta el flujo de trabajo de bajo nivel necesario para la compilación cruzada y la inyección de código en memoria.

## Requisitos del Entorno

Para la generación de los binarios destinados al procesador RISC-V, es imprescindible disponer de una cadena de herramientas de compilación cruzada específica. Este proyecto utiliza xPack GNU RISC-V Embedded GCC. Antes de proceder con la compilación, debe descargar la herramienta desde el repositorio oficial (https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/) y asegurar que las rutas de los binarios coincidan con las utilizadas en los scripts de este documento.

## Estructura del Repositorio y Lógica de Ejecución

El proyecto se organiza en directorios temáticos correspondientes a cada tipo de prueba de estrés: Numeros_Primos, Producto_decimales y Producto_Matrices. La estructura de cada directorio está diseñada para separar el código del procesador anfitrión (ARM) del código del dispositivo (RISC-V).

En el nivel superior de cada carpeta se encuentran los archivos fuente principales: Calculo_Primos.c, Producto_decimales.c y Producto_matrices.c. Estos archivos constituyen la aplicación maestra que debe importarse y ejecutarse en el entorno Xilinx Vitis. Este código se ejecuta sobre el procesador ARM Cortex-A9 y tiene una doble función. En primer lugar, ejecuta el algoritmo de prueba de forma nativa en el ARM para establecer una línea base de rendimiento. En segundo lugar, actúa como orquestador del sistema: se encarga de mantener al núcleo RISC-V en estado de reset, copiar el firmware hexadecimal en la memoria compartida y liberar el reset para iniciar la ejecución en el coprocesador, cronometrando posteriormente el tiempo que este tarda en completar la misma tarea.

Dentro de cada directorio principal existe una subcarpeta denominada Conversion_Hexadecimal. Este directorio contiene el entorno de desarrollo exclusivo para el núcleo RISC-V. Aquí residen los archivos fuente adaptados para ejecución bare-metal (como firmware_simple.c o firmware.c), el código de arranque (start.s) y los scripts de enlace. Es en esta ubicación donde se debe realizar la compilación cruzada para obtener el array de datos que posteriormente consumirá el ARM.

## Instrucciones de Compilación y Generación de Hexadecimales

Para que la aplicación del ARM en Vitis pueda cargar el programa del RISC-V, es necesario transformar el código C de la subcarpeta Conversion_Hexadecimal en un array hexadecimal. Este proceso consta de tres pasos que deben ejecutarse desde la línea de comandos dentro de dicha subcarpeta.

El primer paso es la Compilación Cruzada, donde se invoca al compilador GCC para generar el archivo ejecutable (.elf) vinculando el código C y el arranque en ensamblador, aplicando las restricciones de memoria definidas en el script de enlace sections.lds.


C:\RISCV\bin\riscv-none-elf-gcc.exe -march=rv32imc -mabi=ilp32 -ffreestanding -nostartfiles -T sections.lds start.s firmware_simple.c -o firmware.elf -lgcc

El segundo paso es la Generación del Binario Puro. Una vez obtenido el archivo ELF, se utiliza la herramienta objcopy para extraer únicamente las instrucciones máquina, descartando metadatos del sistema operativo para obtener un archivo .bin crudo.

C:\RISCV\bin\riscv-none-elf-objcopy.exe -O binary firmware.elf firmware.bin

El tercer paso es la Generación del Header. Se ejecuta el script de PowerShell convertir.ps1, el cual lee el archivo binario y genera un archivo de cabecera llamado firmware.h.

./convertir.ps1

El contenido de este archivo firmware.h generado contiene el código máquina del RISC-V formateado como un array de C. Este contenido debe ser copiado e integrado dentro del código fuente principal del ARM (los archivos .c de la carpeta superior mencionados anteriormente) en Xilinx Vitis, permitiendo así que el procesador anfitrión inyecte el programa en la memoria del RISC-V durante la ejecución.
