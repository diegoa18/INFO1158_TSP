import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(f"CWD: {os.getcwd()}")
print(f"Sys Path: {sys.path}")

from core.loader import load_cities
from core.distance import distance_matrix
from core.graph import Graph
from visualization.plot_graph import plot_complete_graph
from visualization.brute_force.animate_brute_force import animate_tsp_brute_force
from visualization.nearest_neighbor.animate_nn import animate_nearest_neighbor
from brute_force.tsp_solver import solve_tsp_brute_force
from brute_force.evaluator import TSPEvaluator
from nearest_neighbor.evaluator import Evaluator as NNEvaluator
from core.paths import ROUTES, FIGS

st.set_page_config(page_title="Visualización TSP", layout="wide")

st.title("Visualización del Problema del Viajante (TSP)")

st.sidebar.header("Configuración")

all_cities = load_cities()
max_cities = len(all_cities)

n_cities = st.sidebar.slider("Número de Ciudades", min_value=3, max_value=max_cities, value=5)

# Cargar ciudades primero para poder seleccionar el origen
cities = load_cities(n_cities=n_cities)
city_names = [c.name for c in cities]

origin_city_name = st.sidebar.selectbox("Ciudad de Origen", city_names)
origin_index = city_names.index(origin_city_name)

if n_cities < 3:
    st.warning("Seleccionar menos de 3 ciudades hace el problema trivial.")
elif n_cities >= 12:
    st.warning("⚠️ Advertencia: Con 12 o más ciudades, el algoritmo de fuerza bruta puede tardar mucho tiempo o no terminar debido a la alta cantidad de iteraciones (factorial).")
elif n_cities > max_cities:
    st.error(f"No se pueden seleccionar más de {max_cities} ciudades.")

if st.sidebar.button("Generar Visualización"):
    st.session_state.generated = True
    st.session_state.run_n_cities = n_cities
    st.session_state.run_origin_index = origin_index
    st.session_state.run_origin_name = origin_city_name

if st.session_state.get("generated", False):
    # Use stored values for generation
    run_n_cities = st.session_state.run_n_cities
    run_origin_index = st.session_state.run_origin_index
    run_origin_name = st.session_state.run_origin_name
    
    # Reload cities based on stored n_cities
    run_cities = load_cities(n_cities=run_n_cities)
    run_dist_matrix = distance_matrix(run_cities)
    run_graph = Graph(run_cities, run_dist_matrix)

    st.header("1. Grafo Estático")
    st.markdown(f"Mostrando grafo completo para **{run_n_cities}** ciudades.")

    fig_placeholder = st.empty()

    def plot_graph_streamlit(cities, D):
        xs = [c.lon for c in cities]
        ys = [c.lat for c in cities]
        names = [c.name for c in cities]
        n = len(cities)

        fig, ax = plt.subplots(figsize=(10, 6))
        
        from matplotlib.collections import LineCollection
        segments = []
        for i in range(n):
            for j in range(i + 1, n):
                segments.append([(cities[i].lon, cities[i].lat), (cities[j].lon, cities[j].lat)])

        lc = LineCollection(segments, linewidths=0.5, colors='blue', alpha=0.3)
        ax.add_collection(lc)

        ax.scatter(xs, ys, s=100, color="red", zorder=5)

        for i, name in enumerate(names):
            ax.text(xs[i] + 0.02, ys[i] + 0.02, name, fontsize=10, zorder=10)

        ax.set_title(f"Grafo Completo (n={n})")
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.autoscale()
        return fig

    fig = plot_graph_streamlit(run_cities, run_dist_matrix)
    st.pyplot(fig)

    st.header("2. Animaciones de Algoritmos")
    st.markdown("Visualizando la ejecución de los algoritmos Fuerza Bruta y Vecino Más Cercano.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Fuerza Bruta")
        bf_gif_path = ROUTES / f"brute_force{run_n_cities}_start{run_origin_index}.gif"
        
        if not bf_gif_path.exists():
            with st.spinner(f"Generando animación Fuerza Bruta para {run_n_cities} ciudades (Origen: {run_origin_name})..."):
                try:
                    result_path = animate_tsp_brute_force(run_n_cities, start_node=run_origin_index)
                    if not result_path or not result_path.exists():
                         st.error("Error al generar animación Fuerza Bruta (función retornó None o archivo faltante).")
                except Exception as e:
                    st.error(f"Error generando animación Fuerza Bruta: {e}")
                
        if bf_gif_path.exists():
            st.image(str(bf_gif_path), caption=f"Fuerza Bruta (n={run_n_cities})")
        else:
            st.warning("Animación Fuerza Bruta no disponible.")

    with col2:
        st.subheader("Vecino Más Cercano")
        nn_gif_path = FIGS / "routes" / f"nearest_neighbor_tour_n{run_n_cities}_start{run_origin_index}.gif"
        
        if not nn_gif_path.exists():
            with st.spinner(f"Generando animación Vecino Más Cercano para {run_n_cities} ciudades (Origen: {run_origin_name})..."):
                try:
                    result_path = animate_nearest_neighbor(run_n_cities, start_node=run_origin_index)
                    if not result_path or not result_path.exists():
                        st.error("Error al generar animación Vecino Más Cercano.")
                except Exception as e:
                     st.error(f"Error generando animación Vecino Más Cercano: {e}")
        
        if nn_gif_path.exists():
            st.image(str(nn_gif_path), caption=f"Vecino Más Cercano (n={run_n_cities})")
        else:
            st.warning("Animación Vecino Más Cercano no disponible.")

    st.header("3. Métricas")
    st.markdown("Comparación de rendimiento entre los dos algoritmos.")

    if st.button("Ejecutar Evaluación"):
        with st.spinner("Evaluando algoritmos..."):
            bf_evaluator = TSPEvaluator()
            # Usar lambda para pasar el start_node
            bf_metrics = bf_evaluator.evaluate(lambda g: solve_tsp_brute_force(g, start_node=run_origin_index), run_graph)
            
            nn_evaluator = NNEvaluator(run_graph)
            nn_metrics = nn_evaluator.evaluate(start_node=run_origin_index)
            
            m_col1, m_col2 = st.columns(2)
            
            with m_col1:
                st.info("Resultados Fuerza Bruta")
                st.metric("Mejor Costo", f"{bf_metrics['best_cost']:.2f}")
                st.metric("Tiempo (s)", f"{bf_metrics['time_seconds']:.6f}")
                st.metric("Iteraciones", f"{bf_metrics['iterations']}")
                st.write("**Mejor Ruta:**")
                st.code(" -> ".join(bf_metrics['best_path_names']))
                
            with m_col2:
                st.info("Resultados Vecino Más Cercano")
                st.metric("Costo", f"{nn_metrics['L_NN']:.2f}")
                st.metric("Tiempo (s)", f"{nn_metrics['time']:.6f}")
                st.metric("Pasos (Ciudades Visitadas)", f"{nn_metrics['steps']}")
                st.write("**Ruta:**")
                st.code(" -> ".join(nn_metrics['route_names']))
                
            st.subheader("Comparación")
            cost_diff = nn_metrics['L_NN'] - bf_metrics['best_cost']
            time_diff = nn_metrics['time'] - bf_metrics['time_seconds']
            iter_diff = nn_metrics['steps'] - bf_metrics['iterations']
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Diferencia de Costo (NN - BF)", f"{cost_diff:.2f}")
            c2.metric("Diferencia de Tiempo (s)", f"{abs(time_diff):.6f}")
            c3.metric("Diferencia de Iteraciones", f"{abs(iter_diff)}")
            
            if bf_metrics['best_cost'] > 0:
                gap = (cost_diff / bf_metrics['best_cost']) * 100
                c4.metric("Brecha de Optimalidad", f"{gap:.2f}%")
            
            if cost_diff == 0:
                st.success("¡Vecino Más Cercano encontró la solución óptima!")
            else:
                st.warning(f"La solución de Vecino Más Cercano es {cost_diff:.2f} unidades más larga que la óptima.")
else:
    st.info("Selecciona la configuración en la barra lateral y presiona 'Generar Visualización' para comenzar.")

