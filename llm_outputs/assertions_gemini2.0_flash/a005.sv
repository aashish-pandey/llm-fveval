assert property (@(posedge clk) disable iff (!rst_n) ((count == 0) |-> empty));
