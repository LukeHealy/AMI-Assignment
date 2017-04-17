function SMA-star(problem): path
  queue: set of nodes, ordered by f-cost;
begin
  queue.insert(problem.root-node);

  while True do begin
    if queue.empty() then return failure; //there is no solution that fits in the given memory
    node := queue.begin(); // min-f-cost-node
    if problem.is-goal(node) then return success;
    
    s := next-successor(node)
    if !problem.is-goal(s) && depth(s) == max_depth then
        f(s) := inf; 
        // there is no memory left to go past s, so the entire path is useless
    else
        f(s) := max(f(node), g(s) + h(s));
        // f-value of the successor is the maximum of
        //      f-value of the parent and 
        //      heuristic of the successor + path length to the successor
    endif
    if no more successors then
       update f-cost of node and those of its ancestors if needed
    
    if node.successors ⊆ queue then queue.remove(node); 
    // all children have already been added to the queue via a shorter way
    if memory is full then begin
      badNode := shallowest node with highest f-cost;
      for parent in badNode.parents do begin
        parent.successors.remove(badNode);
        if needed then queue.insert(parent); 
      endfor
    endif

    queue.insert(s);
  endwhile
end