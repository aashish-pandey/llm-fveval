property p_wr_en_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 wr_en |-> !full;
endproperty

assert property (p_wr_en_check) else $error("Write enable when FIFO is full");

property p_rd_en_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 rd_en |-> !empty;
endproperty

assert property (p_rd_en_check) else $error("Read enable when FIFO is empty");

property p_count_update;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 do_wr -> count == count + 1'b1;

do_rd -> count == count - 1'b1;

default : count == count;
endproperty

assert property (p_count_update) else $error("Incorrect count update");

property p_empty_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 empty == (count == 0);
endproperty

assert property (p_empty_check) else $error("Empty flag incorrect");

property p_full_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 full == (count == DEPTH);
endproperty

assert property (p_full_check) else $error("Full flag incorrect");

