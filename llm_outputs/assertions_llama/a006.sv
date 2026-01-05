assert property (
@(posedge clk)
  disable iff (!rst_n)
    full |=> wr_ptr == DEPTH - 1;
);
