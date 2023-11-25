soluciones = []
CANTIDAD_MAX_ITER = 5000
cantidad_iter = 0
import math


def main():

    capacidad = -1 # Define tu capacidad máxima
    ubicaciones = {}
    demandas = {}
    distancias = []
    dimension = -1
    with open("ciudades_con_numeros.txt", "r") as file:
        line = file.readline()
        while line:
            if line.startswith("NODE_COORD_SECTION"):
                line = file.readline()
                while not line.startswith("EOF"):
                    numero_sucursal = int(line.split(" ")[0])
                    
                    posicion_x = float(line.split(" ")[1])
                    posicion_y = float(line.split(" ")[2])
                    ubicaciones[numero_sucursal] = (posicion_x, posicion_y)
                    line = file.readline()
            elif line.startswith("DIMENSION"):
                dimension = int(line.split(":")[1])
            line = file.readline()

        # calcular distancias de todas con todas
        for i in range(dimension):
            distancias.append([])
            for j in range(dimension):
                distancias[i].append(calcular_distancia(i + 1, j + 1, ubicaciones))
        for sucursal in ubicaciones.keys():
            print("Sucursal: ", sucursal)
            resolver_tsp_thread(sucursal, ubicaciones, soluciones, distancias)


        print("Soluciones: ", soluciones)
        soluciones.sort(key=lambda x: x[1])
        with open("solucion.txt", "w") as file:
            print(soluciones)
            # escribir sucursales según orden de visita separando por espacio
            file.write(" ".join([str(x) for x in soluciones[0][0]]))
            print(soluciones[0][1])


import math

def resolver_tsp_thread(sucursal, ubicaciones, soluciones, distancias):
    ruta_optima = resolver_tsp(sucursal, ubicaciones, distancias)
    if not ruta_optima:
        return
    distancia_total = calcular_distancia_total(ruta_optima, ubicaciones)
    soluciones.append((ruta_optima, distancia_total))


def calcular_distancia_total(ruta_optima, ubicaciones):
    distancia_total = 0
    for i in range(len(ruta_optima) - 1):
        ubicacion1 = ruta_optima[i]
        ubicacion2 = ruta_optima[i + 1]
        distancia_total += calcular_distancia(ubicacion1, ubicacion2, ubicaciones)
    return distancia_total

# Función para calcular la distancia entre dos ubicaciones (sucursales)
def calcular_distancia(ubicacion1, ubicacion2, ubicaciones):
    ubicacion1 = ubicaciones[ubicacion1]
    ubicacion2 = ubicaciones[ubicacion2]
    x1, y1 = ubicacion1
    x2, y2 = ubicacion2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Función para encontrar la ubicación más cercana no visitada
def encontrar_ubicacion_mas_cercana(ubicacion_actual, ubicaciones_no_visitadas, ubicaciones, distancias):
    distancia_minima = float('inf')
    ubicacion_cercana = None
    for ubicacion in ubicaciones_no_visitadas:
        distancia = distancias[ubicacion_actual - 1][ubicacion - 1]

        if distancia < distancia_minima:
            distancia_minima = distancia
            ubicacion_cercana = ubicacion

    return ubicacion_cercana

# Función para resolver el tsp usando un enfoque greedy
def resolver_tsp(sucursal_origen, ubicaciones, distancias):
    ruta_optima = []
    ubicacion_actual = sucursal_origen  # Partimos desde la central
    ubicaciones_no_visitadas = list(ubicaciones.keys())
    ubicaciones_no_visitadas.remove(sucursal_origen)  # Sacamos la central visitada recientemente

    while ubicaciones_no_visitadas:
        ubicacion_cercana = encontrar_ubicacion_mas_cercana(ubicacion_actual, ubicaciones_no_visitadas, ubicaciones, distancias)
        print(ubicacion_cercana)
        if ubicacion_cercana is None:
            break

        ruta_optima.append(ubicacion_cercana)
        ubicacion_actual = ubicacion_cercana
        ubicaciones_no_visitadas.remove(ubicacion_cercana)


    if len(ubicaciones_no_visitadas) > 0:
        return []
    
    # Volver a la central (sucursal origen)
    ruta_optima.append(sucursal_origen)
    return ruta_optima





    


if __name__ == "__main__":
    main()