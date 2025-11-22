#ORQUESTADOR BRUTE FORCE LOCAL
import sys
import os

#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.loader import load_cities
from core.graph import Graph
from core.distance import distance_matrix
from brute_force.tsp_solver import solve_tsp_brute_force
from brute_force.evaluator import TSPEvaluator

def run():    
    try:
        cities = load_cities("cities.csv")
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    #matriz y grafo
    dist_matrix = distance_matrix(cities)
    graph = Graph(cities, dist_matrix)

    #evaluador
    evaluator = TSPEvaluator()
    results = evaluator.evaluate(solve_tsp_brute_force, graph)
    
    #metricas
    print(f"Optimal Cost (L*): {results['best_cost']:.4f}")
    print(f"Optimal Path (pi*): {results['best_path']}")
    path_str = " -> ".join(results['best_path_names'])
    print(f"Optimal Path (pi*): {path_str}")
    print(f"Time Taken: {results['time_seconds']:.4f} seconds")
    print(f"Total Iterations: {results['iterations']}")

#if __name__ == "__main__":
 #   run()
