#tranquilo, ya viene
#from typing import List, Tuple
from core.graph import Graph
from core.types import City
from core.paths import ROUTES
import math
import numpy
import matplotlib.pyplot as plt

from typing import List, Tuple, Optional

#funcion de vecino mas cercano
# graph : es el grafo que tiene las ciudades y la matriz de distancia
# start: es por donde parte

def nearest_neighbor_algorithm(
        graph: Graph,
        start: int = 0 ) -> Tuple[List[int], float]:
    
    n = graph.n # el numero de ciudades

    # Verificaciones
    if n == 0:
        print("Graph has no cities")
        raise ValueError("Graph has no cities")
    
    if not (0 <= start < n):
        print("Start index must be in range")
        raise ValueError("Start index must be in range")

    # Ciudades visitadas
    cities_visited = [False] * n
    cities_visited[start] = True

    # Ruta que va a ser construida
    tour: List[int] = [start]
    
    total_length: float = 0.0
    current_city: int = start

    # Se busca el vecino no visitado más cercano
    for _ in range(n - 1):
        best_city: Optional[int] = None
        best_length: float = float('inf')

        for k in range(n):
            if cities_visited[k]:
                continue

            dist = graph.get_distance(current_city, k)

            if dist < best_length:
                best_length = dist
                best_city = k
        
        if best_city is None:
            break # esto pasa si la ciudad no tiene vecinos, ojala no pase :3

        # Nos movemos a la ciudad más cercana
        tour.append(best_city)
        cities_visited[best_city] = True
        total_length += best_length
        current_city = best_city

    # Retorno a la ciudad inicial
    return_dist = graph.get_distance(current_city, start)
    tour.append(start)
    total_length += return_dist

    #va a devolver la ruta y la longitud total
    return tour, total_length


    



        




    

    

    



