#consume el generador del solver, mide tiempo, cuenta iteraciones y retorna metricas
import time
from typing import Callable, Dict, Any, List, Tuple, Iterator
from core.graph import Graph

class TSPEvaluator:
    def evaluate(self,#solver_func recibe un graph y retorna un generador de tuplas (tsp_solver)
                solver_func: Callable[[Graph], Iterator[Tuple[List[int], float, List[int], float]]],
                graph: Graph) -> Dict[str, Any]:


        start_time = time.perf_counter() #tiempo transcurrido
        
        best_cost = float('inf')
        best_path = None
        iterations = 0
        
        for _, _, b_path, b_cost in solver_func(graph): #recorrer el generador
            #actualizacion de mejores resultados
            best_cost = b_cost
            best_path = b_path
            iterations += 1
            
        #tiempo transcurrido final
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        return {
            "best_cost": best_cost,
            "best_path": best_path,
            "best_path_names": [graph.get_city_name(i) for i in best_path],
            "time_seconds": duration,
            "iterations": iterations
        }
