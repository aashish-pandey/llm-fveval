assert property (p_wr_en_check) else $error("Write enable when FIFO is full");

property p_rd_en_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 rd_en |-> !empty;
endproperty
