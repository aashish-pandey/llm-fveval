```systemverilog
module llm_assertions;
  // Write interface is not empty on reset.
  @(posedge clk)
  disable iff (!rst_n)
    wr_en |=> ~empty;

  // Write data is valid before being written to memory.
  @(posedge clk)
  disable iff (!rst_n)
    (wr_en & !full) |=> $past(wr_data);

  // Data read from FIFO is what was previously written.
  @(posedge clk)
  disable iff (!rst_n)
    ((rd_en & !empty) |-> rd_data == $past(mem[rd_ptr]));

  // Count update due to write only happens on a valid wr ptr.
  @(posedge clk)
  disable iff (!rst_n)
    (do_wr |=> wr_ptr + 1'b1 == wr_ptr);

  // Count update due to read only happens on a valid rd ptr.
  @(posedge clk)
  disable iff (!rst_n)
    (do_rd |=> rd_ptr + 1'b1 == rd_ptr);

  // Full flag is set when the write pointer is at the end of memory.
  @(posedge clk)
  disable iff (!rst_n)
    full |=> wr_ptr == DEPTH - 1;

  // Empty flag is reset when the read pointer is at the start of memory.
  @(posedge clk)
  disable iff (!rst_n)
    !empty |=> rd_ptr != '0;
endmodule
```

