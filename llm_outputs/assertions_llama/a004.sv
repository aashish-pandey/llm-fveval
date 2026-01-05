assert property (
@(posedge clk)
  disable iff (!rst_n)
    (do_wr |=> wr_ptr + 1'b1 == wr_ptr);
);
