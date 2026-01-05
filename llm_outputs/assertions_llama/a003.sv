assert property (
@(posedge clk)
  disable iff (!rst_n)
    ((rd_en & !empty) |-> rd_data == $past(mem[rd_ptr]));
);
