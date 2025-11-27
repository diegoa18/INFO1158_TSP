import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection # pa dibujar lineas
import numpy as np
from typing import List, Optional
from core.paths import FIGS
from core.types import City

#dibuja el grafo completo con todas las cuiades
def plot_complete_graph(cities: List[City], D: np.ndarray, save_path: Optional[str] = None) -> None:
    xs = [c.lon for c in cities] #lon
    ys = [c.lat for c in cities] #lat
    names = [c.name for c in cities]
    n = len(cities)

    plt.figure(figsize=(10, 8))

    #lineas entre todas las ciudades
    segments = []
    for i in range(n):
        for j in range(i + 1, n):
            segments.append([(cities[i].lon, cities[i].lat), (cities[j].lon, cities[j].lat)])

    lc = LineCollection(segments, linewidths=0.5, colors='blue', alpha=0.5)
    plt.gca().add_collection(lc)

    #dibuja los nodos
    plt.scatter(xs, ys, s=100, color="red", zorder=5)

    #etiquetas
    for i, name in enumerate(names):
        plt.text(xs[i] + 0.02, ys[i] + 0.02, name, fontsize=10, zorder=10)

    plt.title("Grafo Completo de Ciudades Seleccionadas")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.autoscale()

    if save_path:
        output_path = FIGS / save_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

    plt.show()