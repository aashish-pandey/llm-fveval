
property p_full_count;
  @(posedge clk) disable iff (!rst_n)
    full |-> count == DEPTH;
endproperty

property p_empty_count;
  @(posedge clk) disable iff (!rst_n)
    empty |-> count == 0;
endproperty

property p_count_transition;
  @(posedge clk) disable iff (!rst_n)
    (do_wr && !do_rd) |-> count == count + 1'b1;
endproperty

property p_count_transition_read;
  @(posedge clk) disable iff (!rst_n)
    (!do_wr && do_rd) |-> count == count - 1'b1;
endproperty

