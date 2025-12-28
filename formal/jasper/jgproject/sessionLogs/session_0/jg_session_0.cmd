#----------------------------------------
# JasperGold Version Info
# tool      : JasperGold 2018.09
# platform  : Linux 5.15.0-164-generic
# version   : 2018.09p001 64 bits
# build date: 2018.11.02 18:06:33 PDT
#----------------------------------------
# started Sun Dec 28 17:19:25 EST 2025
# hostname  : ece-rh810-10
# pid       : 1682069
# arguments : '-label' 'session_0' '-console' 'ece-rh810-10:45031' '-nowindow' '-style' 'windows' '-exitonerror' '-data' 'AQAAADx/////AAAAAAAAA3oBAAAAEABMAE0AUgBFAE0ATwBWAEU=' '-proj' '/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval/formal/jasper/jgproject/sessionLogs/session_0' '-init' '-hidden' '/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval/formal/jasper/jgproject/.tmp/.initCmds.tcl' 'run_fpv.tcl' '-hidden' '/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval/formal/jasper/jgproject/.tmp/.postCmds.tcl'
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
