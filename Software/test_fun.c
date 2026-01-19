#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"

// DIRECCIONES DEL HARDWARE
#define BRAM_BASE_ADDR   0x40000000
#define GPIO_RESET_ADDR  0x41200000

int main()
{
    init_platform();
    print("--- INICIANDO TEST DE HARDWARE ---\n\r");

    // 1. TEST DE MEMORIA COMPARTIDA (BRAM)
    print("Probando BRAM... ");
    u32 test_val = 0x12345678; // Un numero cualquiera

    // Escribimos en la direccion 0x40000000
    Xil_Out32(BRAM_BASE_ADDR, test_val);

    // Leemos de la misma direccion
    u32 read_val = Xil_In32(BRAM_BASE_ADDR);

    if (read_val == test_val) {
        print("OK! (Lectura coincide con Escritura)\n\r");
    } else {
        print("ERROR! La BRAM no responde correctamente.\n\r");
    }

    // 2. TEST DEL INTERRUPTOR (GPIO RESET)
    print("Probando GPIO Reset... ");

    // Escribimos un 1 (Encender)
    Xil_Out32(GPIO_RESET_ADDR, 1);
    u32 gpio_val = Xil_In32(GPIO_RESET_ADDR);

    // Leemos el registro (el bit 0 deberia estar a 1)
    if ( (gpio_val & 1) == 1 ) {
        print("OK! (El GPIO mantiene el valor 1)\n\r");
    } else {
        print("ERROR! El GPIO no guardo el estado.\n\r");
    }

    // 3. APAGAR TODO
    Xil_Out32(GPIO_RESET_ADDR, 0); // Dejar el RISC-V en Reset
    print("--- TEST FINALIZADO ---\n\r");

    cleanup_platform();
    return 0;
}
