import time
from typing import Callable, Dict, Any, List, Tuple, Iterator
from core.graph import Graph

class TSPEvaluator:
    def evaluate(self, solver_func: Callable[[Graph],
                Iterator[Tuple[List[int], float, List[int], float]]],
                graph: Graph) -> Dict[str, Any]:


        start_time = time.perf_counter()
        
        best_cost = float('inf')
        best_path = None
        iterations = 0
        
        for _, _, b_path, b_cost in solver_func(graph):
            best_cost = b_cost
            best_path = b_path
            iterations += 1
            
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        return {
            "best_cost": best_cost,
            "best_path": best_path,
            "time_seconds": duration,
            "iterations": iterations
        }
