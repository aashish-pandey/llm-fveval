assert property (@(posedge clk) disable iff (!rst_n) (rd_ptr >= 0 && rd_ptr < 8));
