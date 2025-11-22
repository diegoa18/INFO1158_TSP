import itertools
from typing import List, Tuple, Iterator, Optional
from core.graph import Graph

def solve_tsp_brute_force(graph: Graph) -> Iterator[Tuple[List[int], 
                                                    float, 
                                                    List[int], 
                                                    float]]:
    n = graph.n
    if n == 0:
        return

    start_node = 0
    other_nodes = list(range(1, n))
    
    best_path: Optional[List[int]] = None
    best_cost = float('inf')
    
    #CICLOS HAMILTONIANOS PARTIENDO DE 0 -> TEMUCOOOOOOO
    for perm in itertools.permutations(other_nodes):
        current_path = [start_node] + list(perm) + [start_node]
        
        current_cost = 0.0
        for k in range(len(current_path) - 1):
            u = current_path[k]
            v = current_path[k+1]
            current_cost += graph.get_distance(u, v)
            
        if current_cost < best_cost:
            best_cost = current_cost
            best_path = list(current_path)
            
        yield current_path, current_cost, best_path, best_cost
