# Root of repo (path is already correct)
set ROOT_DIR [file normalize [file join [pwd] ../..]]

# Analyze RTL + assertions (Jasper 2018 uses analyze, NOT read_*)
analyze -sv \
  $ROOT_DIR/rtl/fifo.sv \
  $ROOT_DIR/formal/jasper/assertion_wrapper.sv


# Elaborate top module
elaborate 

# Clock and reset
clock clk
reset -expression {!rst_n}

# Prove all properties
prove -all

# Reports
report -summary
report 

# Exit
exit
