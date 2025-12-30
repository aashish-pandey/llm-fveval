property p_not_full_and_empty;
  @(posedge clk) disable iff (!rst_n)
    !(full && empty);
endproperty
