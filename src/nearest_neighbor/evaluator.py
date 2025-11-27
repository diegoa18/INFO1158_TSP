import sys
import os

#agrega el src para importar las cosas, lo mismo pal siguiente archivo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import time
from typing import Dict, Any, List
from core.graph import Graph
from nearest_neighbor.nearest_neighbor import nearest_neighbor_algorithm

class Evaluator:
    def __init__(self, graph: Graph):
        self.graph = graph

    #pa evaluar el algoritmo
    def evaluate(self, start_node: int = 0) -> Dict[str, Any]:
        
        start_time = time.perf_counter()
        
        #se corre el algoritmo
        tour, length = nearest_neighbor_algorithm(self.graph, start=start_node)
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        #cantidad de iteraciones 
        steps = len(tour) - 1
        
        best_path_names = [self.graph.get_city_name(i) for i in tour]
        
        #devuelvo un dicc con la informacion
        return {
            "algorithm": "Nearest Neighbor",
            "pi_NN": tour,
            "L_NN": length,
            "route_names": best_path_names,
            "time": elapsed_time,
            "steps": steps
        }
