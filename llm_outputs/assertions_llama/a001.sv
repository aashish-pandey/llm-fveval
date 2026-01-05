assert property (
@(posedge clk)
  disable iff (!rst_n)
    wr_en |=> ~empty;
);
