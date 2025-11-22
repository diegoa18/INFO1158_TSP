import sys
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import numpy as np

# Add src to python path to allow imports from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph
from core.paths import FIGS
from nearest_neighbor.nearest_neighbor import nearest_neighbor_algorithm

def animate_nearest_neighbor():
    # 1. Load Data
    print("Loading data...")
    cities = load_cities()
    D = distance_matrix(cities)
    graph = Graph(cities, D)
    
    # 2. Run Algorithm
    print("Running Nearest Neighbor Algorithm...")
    tour, length = nearest_neighbor_algorithm(graph, start=0)
    
    # 3. Prepare Visualization
    xs = [c.lon for c in cities]
    ys = [c.lat for c in cities]
    names = [c.name for c in cities]
    n = len(cities)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plot all cities initially
    ax.scatter(xs, ys, s=100, color="#E0E0E0", zorder=5, label="Cities") # Light gray for unvisited
    
    # Labels
    for i, name in enumerate(names):
        ax.text(xs[i] + 0.02, ys[i] + 0.02, name, fontsize=9, color="#555555", zorder=10)

    # Setup for animation
    lines = []
    scat = ax.scatter([], [], s=150, color="#FF5722", zorder=20, label="Current City") # Orange for current
    
    # Path collection
    lc = LineCollection([], linewidths=2, colors='#2196F3', alpha=0.8, zorder=15) # Blue path
    ax.add_collection(lc)
    
    # Title and info
    title_text = ax.text(0.5, 1.02, "", transform=ax.transAxes, ha="center", fontsize=14, weight='bold')
    info_text = ax.text(0.02, 0.98, "", transform=ax.transAxes, ha="left", va="top", fontsize=12, 
                        bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8))

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='lower right')
    
    # Set limits with some padding
    ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
    ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)

    def init():
        lc.set_segments([])
        scat.set_offsets(np.empty((0, 2)))
        title_text.set_text("Nearest Neighbor Algorithm Initialization")
        info_text.set_text("Starting...")
        return lc, scat, title_text, info_text

    def update(frame):
        # frame goes from 0 to len(tour) - 1
        # In each frame, we show the path up to that point
        
        current_path_indices = tour[:frame+1]
        current_city_idx = tour[frame]
        
        # Update path segments
        segments = []
        current_dist = 0.0
        
        if len(current_path_indices) > 1:
            for i in range(len(current_path_indices) - 1):
                u = current_path_indices[i]
                v = current_path_indices[i+1]
                segments.append([(cities[u].lon, cities[u].lat), (cities[v].lon, cities[v].lat)])
                current_dist += graph.get_distance(u, v)
        
        lc.set_segments(segments)
        
        # Update current city marker
        current_city = cities[current_city_idx]
        scat.set_offsets([[current_city.lon, current_city.lat]])
        
        # Update texts
        title_text.set_text(f"Step {frame}: Visiting {current_city.name}")
        info_text.set_text(f"Total Distance: {current_dist:.2f}\nCities Visited: {frame + 1}/{n}")
        
        # Highlight visited cities (optional, maybe change color of visited points)
        # For now, just the path and current city is enough for clarity
        
        return lc, scat, title_text, info_text

    # Create animation
    # Frames: we want to show each step. tour has n+1 indices (start ... start)
    anim = animation.FuncAnimation(fig, update, frames=len(tour), init_func=init, blit=True, interval=500, repeat_delay=2000)
    
    # Save
    output_path = FIGS / "routes" / "nearest_neighbor_tour.gif"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving animation to {output_path}...")
    anim.save(output_path, writer='pillow', fps=2)
    print("Done!")

if __name__ == "__main__":
    animate_nearest_neighbor()
