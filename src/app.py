from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph
from visualization.plot_graph import plot_complete_graph

#TESTEO
def main():
    cities = load_cities()
    D = distance_matrix(cities)
    graph = Graph(cities, D)
    print(graph)
    print(D)
    plot_complete_graph(cities, D, save_path="complete_graph.png")

if __name__ == "__main__":
    main()