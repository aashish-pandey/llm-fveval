assert property (@posedge clk; !full_queue implies ##[*:$] rst_n) always @(negedge clk);
