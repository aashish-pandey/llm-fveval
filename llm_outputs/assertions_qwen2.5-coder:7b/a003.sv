property p_count_transition;
  @(posedge clk) disable iff (!rst_n)
    (do_wr && !do_rd) |-> count == count + 1'b1;
endproperty
