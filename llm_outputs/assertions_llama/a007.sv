assert property (
@(posedge clk)
  disable iff (!rst_n)
    !empty |=> rd_ptr != '0;
);
