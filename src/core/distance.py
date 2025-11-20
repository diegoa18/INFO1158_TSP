import math

def euclidean(coord1, coord2): #DISTANCIA EUCLIDIANA (GRADOS, NO KILOMETROS)
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    #DISTANCIA EUCLIDIANA 2D
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def distance_matrix(cities): #MATRIZ DE DISTANCIAS "D"
    n = len(cities)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)] #LLENA DE 0

    for i in range(n): #SE LLENA LOL
        for j in range(n):
            coord1 = (cities[i]["lat"], cities[i]["lon"])
            coord2 = (cities[j]["lat"], cities[j]["lon"])
            matrix[i][j] = euclidean(coord1, coord2)

    return matrix