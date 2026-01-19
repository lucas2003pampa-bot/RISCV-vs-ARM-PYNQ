`timescale 1 ns / 1 ps

module tb_riscv;

    // --- SEÑALES ---
    reg clk = 0;
    reg resetn = 0;        // Reset activo bajo (0 = reseteando, 1 = funcionando)
    reg mem_ready = 0;     // Dice al procesador "el dato está listo"
    reg [31:0] mem_rdata = 0; // Datos que enviamos al procesador
    
    wire mem_valid;        // El procesador pide algo
    wire [31:0] mem_addr;  // Dirección que pide
    wire [31:0] mem_wdata; // Dato que quiere escribir
    wire [3:0] mem_wstrb;  // Máscara de escritura

    // --- INSTANCIA DEL PROCESADOR (DUT) ---
    picorv32 uut (
        .clk(clk),
        .resetn(resetn),
        .mem_valid(mem_valid),
        .mem_ready(mem_ready),
        .mem_addr(mem_addr),
        .mem_wdata(mem_wdata),
        .mem_wstrb(mem_wstrb),
        .mem_rdata(mem_rdata)
    );

    // --- GENERADOR DE RELOJ (100 MHz) ---
    always #5 clk = ~clk; // Cambia cada 5ns -> periodo 10ns

    // --- SIMULACIÓN DE MEMORIA SIMPLE ---
    // Si el procesador pide algo, esperamos 1 ciclo y se lo damos
    always @(posedge clk) begin
        if (resetn && mem_valid && !mem_ready) begin
            mem_ready <= 1;
            mem_rdata <= 32'h00000013; // Instrucción NOP (No Operation)
        end else begin
            mem_ready <= 0;
        end
    end

    // --- EL GUIÓN DE LA PRUEBA ---
    initial begin
        $display("--- INICIO DE LA SIMULACIÓN ---");
        
        // 1. Mantenemos reset pulsado un rato
        resetn = 0;
        #100; // Esperar 100ns
        
        // 2. Soltamos reset (Arranca el procesador)
        $display("--- Liberando Reset ---");
        resetn = 1;
        
        // 3. Dejamos correr el tiempo para ver si hace algo
        #2000;
        
        $display("--- FIN DE LA SIMULACIÓN ---");
        $finish;
    end

endmodule
