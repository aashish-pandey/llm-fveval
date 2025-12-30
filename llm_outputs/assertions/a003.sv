assert property (p_count_update) else $error("Incorrect count update");

property p_empty_check;
 @(posedge clk or negedge rst_n)
 disable iff (!rst_n)
 empty == (count == 0);
endproperty
