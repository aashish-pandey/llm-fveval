module llm_assertions;

  // Count must never go negative or exceed DEPTH
  property p_count_in_range;
    @(posedge clk)
      disable iff (!rst_n)
      (count <= DEPTH);
  endproperty

  assert property (p_count_in_range);

endmodule
