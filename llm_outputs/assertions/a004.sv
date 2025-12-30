assert property (p_empty_check) else $error("Empty flag incorrect");

property p_full_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 full == (count == DEPTH);
endproperty
