import matplotlib.pylab as plt
from core.paths import FIGS

def plot_complete_graph(cities, D, save_path=None):
    xs = [c["lon"] for c in cities]   #lon
    ys = [c["lat"] for c in cities]   #lat
    names = [c["name"] for c in cities]

    plt.figure(figsize=(9, 7))

    #DIBUJAR ARISTAS
    n = len(cities)
    for i in range(n):
        for j in range(i+1, n):
            plt.plot(
                [cities[i]["lon"], cities[j]["lon"]],
                [cities[i]["lat"], cities[j]["lat"]],
                linewidth=0.5
            )

    #DIBUJAR NODOS
    plt.scatter(xs, ys, s=100, color="red")

    #ETIQUETAS
    for i, name in enumerate(names):
        plt.text(xs[i] + 0.02, ys[i] + 0.02, name, fontsize=10)

    plt.title("GRAFO COMPLETO CIUDADES SELECCIONADAS")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True)

    if save_path:
        save_path = FIGS / save_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)


    plt.show()