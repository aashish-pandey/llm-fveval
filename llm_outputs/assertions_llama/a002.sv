assert property (
@(posedge clk)
  disable iff (!rst_n)
    (wr_en & !full) |=> $past(wr_data);
);
