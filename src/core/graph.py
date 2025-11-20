from typing import List
import numpy as np
from .types import City

#REPRESANTACION DE GRAFO COMPLETO
class Graph:
    def __init__(self, cities: List[City], distance_matrix: np.ndarray):
        self.cities = cities
        self.names = [c.name for c in cities]
        self.D = distance_matrix
        self.n = len(cities)

    def get_distance(self, i: int, j: int) -> float:
        return self.D[i, j]
    
    def get_city_name(self, i: int) -> str:
        return self.names[i]
    
    def __repr__(self) -> str:
        return f"Graph(n={self.n}, cities={self.names})"
