import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph
from brute_force.tsp_solver import solve_tsp_brute_force
from core.paths import ROUTES

def animate_tsp_brute_force(n_cities: int = None, start_node: int = 0):
    #cargar datos
    try:
        cities = load_cities(n_cities=n_cities)
    except FileNotFoundError:
        print("Error: cities.csv not found.")
        return None

    n = len(cities)
    
    if n < 2:
        print("Not enough cities for TSP.")
        return None
    
    #crear grafo
    dist_matrix = distance_matrix(cities)
    graph = Graph(cities, dist_matrix)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    xs = [c.lon for c in cities]
    ys = [c.lat for c in cities]
    names = [c.name for c in cities]
    
    #dibujar nodos (ciudades) - estático
    ax.scatter(xs, ys, s=100, color="blue", zorder=5, label='Cities')
    for i, name in enumerate(names):
        ax.text(xs[i] + 0.02, ys[i] + 0.02, name, fontsize=9, zorder=10)
        
    ax.set_title(f"TSP Brute Force Animation (n={n})")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    #elementos dinamicos
    current_line_collection = LineCollection([], linewidths=1, colors='gray', linestyle='dashed', alpha=0.7, label='Current Cycle')
    best_line_collection = LineCollection([], linewidths=2, colors='red', alpha=1.0, label='Best Cycle')
    ax.add_collection(current_line_collection)
    ax.add_collection(best_line_collection)
    
    #textos de estado
    status_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, verticalalignment='top', fontsize=10, 
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    #leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='blue', marker='o', linestyle='None', label='Cities'),
        Line2D([0], [0], color='gray', linestyle='--', label='Current Cycle'),
        Line2D([0], [0], color='red', linewidth=2, label='Best Cycle')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    ax.autoscale()
    
    #generador
    solver_gen = solve_tsp_brute_force(graph, start_node=start_node)
    
    def update(frame_data):
        current_path, current_cost, best_path, best_cost = frame_data
        
        #actualizacion grafica de current_path
        if current_path:
            segments_current = []
            for k in range(len(current_path) - 1):
                u_idx = current_path[k]
                v_idx = current_path[k+1]
                segments_current.append([(cities[u_idx].lon, cities[u_idx].lat), 
                                         (cities[v_idx].lon, cities[v_idx].lat)])
            current_line_collection.set_segments(segments_current)
            
        #actualizacion grafica de best_path
        if best_path:
            segments_best = []
            for k in range(len(best_path) - 1):
                u_idx = best_path[k]
                v_idx = best_path[k+1]
                segments_best.append([(cities[u_idx].lon, cities[u_idx].lat), 
                                      (cities[v_idx].lon, cities[v_idx].lat)])
            best_line_collection.set_segments(segments_best)
            
        #actualizacion de texto
        status_text.set_text(f"Current Cost: {current_cost:.2f}\nBest Cost: {best_cost:.2f}")
        
        return current_line_collection, best_line_collection, status_text

    #calcular frames
    import math
    total_frames = math.factorial(n - 1)
    
    if total_frames < 500:
        sample_rate = 1
    else:
        sample_rate = total_frames // 200 #200FRAMES
        
    # Convertir a lista para evitar problemas con generadores vacíos o de un solo elemento en FuncAnimation
    sampled_frames = list(frame for i, frame in enumerate(solver_gen) if i % sample_rate == 0)

    if not sampled_frames:
        print("No frames generated.")
        return None

    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=sampled_frames, 
        interval=500 if n <= 3 else 50, # Más lento para pocos nodos 
        blit=True, 
        repeat=False)
    
    #ruta del gif
    output_file = ROUTES / f"brute_force{n}_start{start_node}.gif"
    print(f"Saving to: {output_file.resolve()}")
    
    try:
        ani.save(output_file, writer='pillow', fps=10)
        print(f"Animation saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving animation: {e}")
        return None