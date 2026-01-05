assert property (@(posedge clk) disable iff (!rst_n) (wr_ptr >= 0 && wr_ptr < 8));
