```systemverilog
module llm_assertions;

  logic clk;
  logic rst_n;
  logic wr_en;
  logic [7:0] wr_data;
  logic full;
  logic rd_en;
  logic [7:0] rd_data;
  logic empty;
  logic [3:0] count;

  default clocking cb @(posedge clk);
  endclocking

  // Assert that when reset is not asserted, the count is never negative.
  assert property (@(posedge clk) disable iff (!rst_n) (count >= 0));

  // Assert that when reset is not asserted, the write pointer is within bounds.
  assert property (@(posedge clk) disable iff (!rst_n) (wr_ptr >= 0 && wr_ptr < 8));

  // Assert that when reset is not asserted, the read pointer is within bounds.
  assert property (@(posedge clk) disable iff (!rst_n) (rd_ptr >= 0 && rd_ptr < 8));

  // Assert that full is asserted when count is equal to DEPTH
  assert property (@(posedge clk) disable iff (!rst_n) ((count == 8) |-> full));

  // Assert that empty is asserted when count is zero
  assert property (@(posedge clk) disable iff (!rst_n) ((count == 0) |-> empty));

endmodule
```