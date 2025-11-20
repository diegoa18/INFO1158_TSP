import logging
from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph
from visualization.plot_graph import plot_complete_graph

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#TESTEO
def main():
    try:
        cities = load_cities()
        D = distance_matrix(cities)
        graph = Graph(cities, D)
        plot_complete_graph(cities, D, save_path="complete_graph.png")

    except FileNotFoundError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()