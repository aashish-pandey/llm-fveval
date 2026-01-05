assert property (@posedge clk; full_queue implies ##[*:$] !full) always @(negedge clk);
