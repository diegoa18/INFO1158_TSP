import sys
import os

# Add src to python path to allow imports from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import time
from typing import Dict, Any, List
from core.graph import Graph
from nearest_neighbor import nearest_neighbor_algorithm

class Evaluator:
    def __init__(self, graph: Graph):
        self.graph = graph

    def evaluate(self) -> Dict[str, Any]:
        # Start from node 0 (Temuco) as requested
        start_node = 0
        
        start_time = time.perf_counter()
        
        # Run Nearest Neighbor algorithm
        tour, length = nearest_neighbor_algorithm(self.graph, start=start_node)
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        # Steps: Number of cities visited (edges traversed)
        steps = len(tour) - 1
        
        best_path_names = [self.graph.get_city_name(i) for i in tour]
        
        return {
            "algorithm": "Nearest Neighbor",
            "pi_NN": tour,
            "L_NN": length,
            "route_names": best_path_names,
            "time": elapsed_time,
            "steps": steps
        }

if __name__ == "__main__":
    print("This module provides the Evaluator class.")
    print("Please run 'src/nearest_neighbor/runner.py' to execute the algorithm and see metrics.")

