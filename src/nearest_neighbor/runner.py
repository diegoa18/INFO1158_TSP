import sys
import os

# Add src to python path to allow imports from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph
from evaluator import Evaluator

def main():
    try:
        # Load data
        print("Loading data...")
        cities = load_cities()
        D = distance_matrix(cities)
        graph = Graph(cities, D)
        n = graph.n
        print(f"Loaded {n} cities.")

        print("Running evaluation...")
        evaluator = Evaluator(graph)
        metrics = evaluator.evaluate()

        # Metrics
        print("\n" + "="*30)
        print("METRICS")
        print("="*30)
        print(f"Algorithm: {metrics['algorithm']}")
        print(f"Steps (Iterations): {metrics['steps']}")
        print(f"Time: {metrics['time']:.6f} seconds")
        print(f"L_NN (Best Cost): {metrics['L_NN']:.4f}")
        print(f"pi_NN (Best Path Indices): {metrics['pi_NN']}")
        print(f"Route Names: {metrics['route_names']}")
        print("="*30)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
