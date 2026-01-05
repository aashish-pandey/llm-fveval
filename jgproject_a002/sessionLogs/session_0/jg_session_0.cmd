#----------------------------------------
# JasperGold Version Info
# tool      : JasperGold 2018.09
# platform  : Linux 5.15.0-164-generic
# version   : 2018.09p001 64 bits
# build date: 2018.11.02 18:06:33 PDT
#----------------------------------------
# started Mon Jan 05 12:04:23 EST 2026
# hostname  : ece-rh810-10
# pid       : 3251235
# arguments : '-label' 'session_0' '-console' 'ece-rh810-10:35355' '-nowindow' '-style' 'windows' '-data' 'AQAAADx/////AAAAAAAAA3oBAAAAEABMAE0AUgBFAE0ATwBWAEU=' '-proj' '/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval/jgproject_a002/sessionLogs/session_0' '-init' '-hidden' '/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval/jgproject_a002/.tmp/.initCmds.tcl' 'compile_only.tcl'
set ROOT_DIR [file normalize [file join [pwd] ../]]


# analyze -sv \
#   $ROOT_DIR/rtl/fifo.sv \
#   $ROOT_DIR/formal/jasper/assertion_wrapper.sv

analyze -sv \
  $ROOT_DIR/rtl/fifo.sv \
  $ROOT_DIR/utils/assertion_wrapper.sv


exit
