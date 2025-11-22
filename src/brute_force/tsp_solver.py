'''Logica pura del algoritmo exhaustivo.
generacion de ciclos hamiltonianos y evaluacion de costos
se utiliza iterator para recorrer la busqueda y generator para la entrega
de resultados'''
import itertools
from typing import List, Tuple, Iterator, Optional
from core.graph import Graph
                                                                    #generador, yield
def solve_tsp_brute_force(graph: Graph) -> Iterator[Tuple[List[int],#->current path
                                                    float,          #->current cost
                                                    List[int],      #->best path
                                                    float]]:        #->best cost
    n = graph.n #n ciudades

    if n == 0:
        return #sin yield

    start_node = 0 #fijar ciudad 0 (temuco), para eliminar rotaciones del mismo ciclo (esto debe ir en el informe 7_7)
    other_nodes = list(range(1, n))
    
    best_path: Optional[List[int]] = None
    best_cost = float('inf')
    
    #CICLOS HAMILTONIANOS DE TEMUCO -> PERM (tupla de ciudades) -> TEMUCO
    for perm in itertools.permutations(other_nodes):
        current_path = [start_node] + list(perm) + [start_node]
        
        current_cost = 0.0 #costo del ciclo actual
        for k in range(len(current_path) - 1):
            u = current_path[k]
            v = current_path[k+1]
            current_cost += graph.get_distance(u, v)
            
        if current_cost < best_cost: #actualizacion de best_path y best_cost
            best_cost = current_cost
            best_path = list(current_path)
            
        yield current_path, current_cost, best_path, best_cost
