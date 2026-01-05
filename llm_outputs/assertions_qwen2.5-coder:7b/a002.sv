property p_empty_count;
  @(posedge clk) disable iff (!rst_n)
    empty |-> count == 0;
endproperty
