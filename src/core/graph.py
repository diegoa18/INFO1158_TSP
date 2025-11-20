#CLASE GRAPH -> GRAFO COMPLETO Kn
class Graph:
    def __init__(self, cities, distance_matrix): #csv de las ciudades y las distancias
        self.cities = cities                        #lista de ciudades 
        self.names = [c["name"] for c in cities]    #lista de nombres
        self.D = distance_matrix                    #matriz de distancias
        self.n = len(cities)                        #cantidad de nodos

    def get_distance(self, i, j):
        return self.D[i][j]
    
    def get_city_name(self, i):
        return self.names[i]
    
    #pa imprimir noma
    def __repr__(self):
        return f"Graph(n={self.n}, cities={self.names})"
