# ==============================================================================
# Automation Script (run.do)
# ==============================================================================

# --- 1. Define Environment Variables & Paths ---
set PROJECT_DIR  "C:/Projects/DigitalDesign"
set RTL_DIR      "$PROJECT_DIR/rtl"
set TB_DIR       "$PROJECT_DIR/tb"
set TOP_LEVEL    "tb_top"

# --- 2. Setup Simulation Library ---
# If the 'work' library already exists, delete it to ensure a clean build
if [file exists work] {
    vdel -lib work -all
}
vlib work
vmap work work

# --- 3. Compile Source Files ---
# Compile Verilog/SystemVerilog RTL files
vlog -work work -sv +incdir+$RTL_DIR "$RTL_DIR/defines.v"
vlog -work work -sv                  "$RTL_DIR/counter.v"
vlog -work work -sv                  "$RTL_DIR/fifo.v"

# Compile Testbench files
vlog -work work -sv +incdir+$TB_DIR  "$TB_DIR/tb_top.sv"

# --- 4. Load Simulation ---
# -voptargs="+acc" preserves visibility for debugging waveforms
vsim -voptargs="+acc" work.$TOP_LEVEL 

# --- 5. Configure Waveforms ---
# Check if GUI is running before managing windows
if {[vsimBool -isgui]} {
    # Open waveform window
    view wave
    
    # Clear existing signals
    delete wave *
    
    # Add clocks and resets (Custom labels and radix)
    add wave -divider "System Control"
    add wave -hex -label "System Clock"   sim:/$TOP_LEVEL/clk
    add wave -bin -label "Reset Active"   sim:/$TOP_LEVEL/rst_n
    
    # Add internal DUT signals using wildcard recursion
    add wave -divider "DUT Interfaces"
    add wave -hex                         sim:/$TOP_LEVEL/dut/*
}

# --- 6. Run Simulation ---
# Log all signals for post-simulation debugging
log -r /*

# Run for a specific time or until $finish
run 100 us

# --- 7. Post-Simulation Report ---
echo "===================================================================="
echo " Simulation Finished at [clock format [clock seconds] -format %T]"
echo "===================================================================="
