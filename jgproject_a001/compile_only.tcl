set ROOT_DIR [file normalize [file join [pwd] ../]]


# analyze -sv \
#   $ROOT_DIR/rtl/fifo.sv \
#   $ROOT_DIR/formal/jasper/assertion_wrapper.sv

analyze -sv \
  $ROOT_DIR/rtl/fifo.sv \
  $ROOT_DIR/utils/assertion_wrapper.sv


exit