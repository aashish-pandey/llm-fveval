property p_fifo_behavior;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 (count == DEPTH) |-> !wr_en;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 (count == 0) |-> !rd_en;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 wr_en && rd_en |-> count == DEPTH;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 wr_en |-> full == (count == DEPTH);
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 rd_en |-> empty == (count == 0);
endproperty

assert_fifo_behavior
  property p_fifo_behavior; endproperty

