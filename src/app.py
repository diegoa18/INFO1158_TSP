from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph

#TESTEO
def main():
    cities = load_cities("data/cities.csv")
    D = distance_matrix(cities)
    graph = Graph(cities, D)
    print(graph)
    print(D)

#if __name__ == "__main__":
 #   main()