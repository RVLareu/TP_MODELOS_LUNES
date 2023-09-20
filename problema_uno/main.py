soluciones = []
CANTIDAD_MAX_ITER = 5000
cantidad_iter = 0
import math

def distancia_entre_cada_una_de_las_sucursales(sucursales):
    """
    Devuelve una matriz con la distancia entre cada una de las sucursales.
    """
    matriz_distancias = []
    for sucursal_uno in sucursales.items():
        matriz_distancias.append([])
        for sucursal_dos in sucursales.items():
            matriz_distancias[-1].append(distancia_entre_sucursales(sucursal_uno[1]["posicion_x"], sucursal_uno[1]["posicion_y"], sucursal_dos[1]["posicion_x"], sucursal_dos[1]["posicion_y"]))
    return matriz_distancias
    


def main():

    sucursales = {}
    capacidad = -1
    dimension = -1

    DISTANCIA_RECORRIDA_ORIGEN = 0
    with open("primer_problema.txt", "r") as file:
        line = file.readline()
        while line:
            if line.startswith("CAPACIDAD"):
                capacidad = int(line.split(":")[1])

            elif line.startswith("DIMENSION"):
                dimension = int(line.split(":")[1])

            elif line.startswith("DEMANDAS"):
                line = file.readline()
                while not line.startswith("FIN DEMANDAS"):
                    numero_sucursal = int(line.split(" ")[0])
                    demanda = int(line.split(" ")[1])
                    sucursales[numero_sucursal] = {"demanda": demanda, "posicion_x": -1, "posicion_y": -1}
                    line = file.readline()
            elif line.startswith("NODE_COORD_SECTION"):
                line = file.readline()
                while not line.startswith("EOF"):
                    numero_sucursal = int(line.split(" ")[0])
                    
                    posicion_x = float(line.split(" ")[1])
                    posicion_y = float(line.split(" ")[2])
                    sucursales[numero_sucursal]["posicion_x"] = math.trunc(posicion_x)
                    sucursales[numero_sucursal]["posicion_y"] = math.trunc(posicion_y)
                    line = file.readline()
            line = file.readline()
    
    matriz_distancias = distancia_entre_cada_una_de_las_sucursales(sucursales)

    for sucursal in sucursales.items():
        if (sucursal[1]["demanda"] >= 0 and sucursal[1]["demanda"] <= capacidad):
            print("Sucursal origen: ", sucursal[0])
            # reinicio cantidad iter para cada sucursal origen
            global cantidad_iter
            cantidad_iter = 0
            resolver(sucursal[1]["demanda"], capacidad, sucursales, [], DISTANCIA_RECORRIDA_ORIGEN, sucursal, matriz_distancias)

    soluciones.sort(key=lambda x: x[1])
    with open("solucion.txt", "w") as file:
        # escribir sucursales según orden de visita separando por espacio
        file.write(" ".join([str(x[0]) for x in soluciones[0][0]]))
        print(soluciones[0][1])




def sucursal_valida(carga_actual, capacidad, sucursales, sucursales_visitadas, sucursal_actual, matriz_distancias):
    """
    Devuelve las n sucursales mas cercanas validas a la actual.
    Valida es que cumpla las restricciones de capacidad y demanda.
    """
    sucursales_validas = []
    for sucursal in sucursales.items():
        if sucursal[0] not in [x[0] for x in sucursales_visitadas] and sucursal[1]["demanda"] + carga_actual <= capacidad and sucursal[1]["demanda"] + carga_actual >= 0:
            sucursales_validas.append(sucursal)
    sucursales_validas.sort(key=lambda x: matriz_distancias[sucursal_actual[0] - 1][x[0] - 1])
    return sucursales_validas[:2]
    


def distancia_entre_sucursales(poxicion_x_sucursal_uno, posicion_y_sucursal_uno, posicion_x_sucursal_dos, posicion_y_sucursal_dos):
    return math.trunc(((poxicion_x_sucursal_uno - posicion_x_sucursal_dos)**2 + (posicion_y_sucursal_uno - posicion_y_sucursal_dos)**2)**(1/2))

def resolver(carga_actual, capacidad, sucursales, sucursales_visitadas, distancia_recorrida, sucursal_actual, matriz_distancias):
    sucursales_visitadas.append(sucursal_actual)
    global cantidad_iter
    cantidad_iter += 1
    if cantidad_iter > CANTIDAD_MAX_ITER:
        return
    if (distancia_recorrida > 8700):
        return False
    if len(sucursales_visitadas) == len(sucursales):
        # Me quedo con la mejor socución
        soluciones.append((sucursales_visitadas.copy(), distancia_recorrida))
        return
    sucursales_validas = sucursal_valida(carga_actual, capacidad, sucursales, sucursales_visitadas, sucursal_actual, matriz_distancias)
    if sucursales_validas is None:
        return False
    for prox_sucursal in sucursales_validas:
        distancia_recorrida += matriz_distancias[sucursal_actual[0] - 1][prox_sucursal[0] - 1]
        carga_actual += sucursales[prox_sucursal[0]]["demanda"]
        if resolver(carga_actual, capacidad, sucursales, sucursales_visitadas, distancia_recorrida, prox_sucursal, matriz_distancias):
            return True
        else:
            distancia_recorrida -= matriz_distancias[sucursal_actual[0] - 1][prox_sucursal[0] - 1]
            carga_actual -= sucursales[prox_sucursal[0]]["demanda"]
            sucursales_visitadas.pop()
    
    return False

if __name__ == "__main__":
    main()