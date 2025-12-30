module llm_assertion_wrapper;

  // DUT signals
  logic clk, rst_n;
  logic wr_en, rd_en;
  logic full, empty;
  logic [7:0] wr_data, rd_data;
  logic [$clog2(8):0] count;

  // Instantiate DUT
  sync_fifo u_dut (
    .clk     (clk),
    .rst_n   (rst_n),
    .wr_en   (wr_en),
    .wr_data (wr_data),
    .full    (full),
    .rd_en   (rd_en),
    .rd_data (rd_data),
    .empty   (empty),
    .count   (count)
  );

  `include "ASSERTION_FILE"
  assert property (ASSERTION_NAME);

  // `include "/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval/llm_outputs/assertions/a005.sv"
  // assert property (p_not_full_and_empty);

    // property p_sanity;
    //   @(posedge clk) disable iff (!rst_n)
    //     1'b1;
    // endproperty

    // assert property (p_sanity);
endmodule
