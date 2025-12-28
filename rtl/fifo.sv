//------------------------------------------------------------------------------
// Simple Synchronous FIFO (single clock)
// - Formal-friendly: explicit pointers + count + full/empty
// - 1 write / 1 read per cycle (can do both in same cycle)
// - DEPTH must be a power of 2
//------------------------------------------------------------------------------

module sync_fifo #(
  parameter int WIDTH = 8,
  parameter int DEPTH = 8   // must be power of 2: 2,4,8,16,...
)(
  input  logic              clk,
  input  logic              rst_n,

  // Write interface
  input  logic              wr_en,
  input  logic [WIDTH-1:0]  wr_data,
  output logic              full,

  // Read interface
  input  logic              rd_en,
  output logic [WIDTH-1:0]  rd_data,
  output logic              empty,

  // Optional observability (great for assertions)
  output logic [$clog2(DEPTH):0] count
);

  localparam int ADDR_W = (DEPTH <= 2) ? 1 : $clog2(DEPTH);

  // Storage
  logic [WIDTH-1:0] mem [0:DEPTH-1];

  // Pointers
  logic [ADDR_W-1:0] wr_ptr, rd_ptr;

  // Qualified ops
  logic do_wr, do_rd;

  // Flags
  always_comb begin
    empty = (count == 0);
    full  = (count == DEPTH);
  end

  // Only perform ops when legal
  always_comb begin
    do_wr = wr_en && !full;
    do_rd = rd_en && !empty;
  end

  // Read data: registered output (more FV/RTL-consistent)
  // rd_data updates on a successful read.
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      rd_data <= '0;
    end else if (do_rd) begin
      rd_data <= mem[rd_ptr];
    end
  end

  // Main sequential logic
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      wr_ptr <= '0;
      rd_ptr <= '0;
      count  <= '0;
    end else begin
      // Write first (safe even if simultaneous read)
      if (do_wr) begin
        mem[wr_ptr] <= wr_data;
        wr_ptr <= wr_ptr + 1'b1;
      end

      if (do_rd) begin
        rd_ptr <= rd_ptr + 1'b1;
      end

      // Count update (handles simultaneous read+write)
      unique case ({do_wr, do_rd})
        2'b10: count <= count + 1'b1; // write only
        2'b01: count <= count - 1'b1; // read only
        default: count <= count;      // none or both
      endcase
    end
  end

  //--------------------------------------------------------------------------
  // (Optional) Elaboration-time sanity check: DEPTH power-of-two
  //--------------------------------------------------------------------------
`ifndef SYNTHESIS
  initial begin
    if (DEPTH < 2) begin
      $fatal(1, "DEPTH must be >= 2");
    end
    if ((DEPTH & (DEPTH - 1)) != 0) begin
      $fatal(1, "DEPTH must be a power of 2. Got DEPTH=%0d", DEPTH);
    end
  end
`endif

endmodule
