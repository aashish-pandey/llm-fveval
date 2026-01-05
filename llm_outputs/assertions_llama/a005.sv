assert property (
@(posedge clk)
  disable iff (!rst_n)
    (do_rd |=> rd_ptr + 1'b1 == rd_ptr);
);
