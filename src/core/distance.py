import numpy as np
from typing import List
from .types import City

def euclidean_matrix(coords: np.ndarray) -> np.ndarray: #DISTANCIA EUCLIDIANA (GRADOS, NO KM)
    delta = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    return np.sqrt(np.sum(delta**2, axis=-1))

def distance_matrix(cities: List[City]) -> np.ndarray:
    coords = np.array([(c.lat, c.lon) for c in cities])
    return euclidean_matrix(coords)