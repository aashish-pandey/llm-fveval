assert property (p_rd_en_check) else $error("Read enable when FIFO is empty");

property p_count_update;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 do_wr -> count == count + 1'b1;

do_rd -> count == count - 1'b1;

default : count == count;
endproperty
