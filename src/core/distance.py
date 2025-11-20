import numpy as np
from typing import List
from .types import City
#DISTANCIA EUCLIDIANA ENTRE TODOS LOS PUNTOS
def euclidean_matrix(coords: np.ndarray) -> np.ndarray:
    #delta[i,j] = coords[i] - coords[j]
    delta = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    #norma euclidiana 2D
    return np.sqrt(np.sum(delta**2, axis=-1))

#CONSTRUCCION DE LA MATRIZ DE DISTANCIAS
def distance_matrix(cities: List[City]) -> np.ndarray:
    coords = np.array([(c.lat, c.lon) for c in cities])
    return euclidean_matrix(coords)