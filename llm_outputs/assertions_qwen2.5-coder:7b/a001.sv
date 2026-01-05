property p_full_count;
  @(posedge clk) disable iff (!rst_n)
    full |-> count == DEPTH;
endproperty
