sucursales = {}
capacidad = -1
dimension = -1
soluciones = []

DISTANCIA_RECORRIDA_ORIGEN = 0


def main():
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
                    sucursales[numero_sucursal]["posicion_x"] = posicion_x
                    sucursales[numero_sucursal]["posicion_y"] = posicion_y
                    line = file.readline()
            line = file.readline()
    for sucursal in sucursales.items():
        if (sucursal[1]["demanda"] >= 0 and sucursal[1]["demanda"] <= capacidad):
            resolver(sucursal[1]["demanda"], capacidad, sucursales, [], DISTANCIA_RECORRIDA_ORIGEN, sucursal)


    soluciones.sort(key=lambda x: x[1])
    with open("solucion.txt", "w") as file:
        # escribir sucursales según orden de visita separando por espacio
        file.write(" ".join([str(x[0]) for x in soluciones[0][0]]))


def sucursales_validas(carga_actual, capacidad, sucursales, sucursales_visitadas):
    """
    Devuelve una lista de sucursales válidas. 
    Una sucursal es valida si su demanda no rompre la restriccion de capacidad y si no fue visitada anteriormente.
    """
    sucursales_validas = []
    for sucursal in sucursales.items():
        if sucursal[0] not in [x[0] for x in sucursales_visitadas] and carga_actual + sucursal[1]["demanda"] <= capacidad and carga_actual + sucursal[1]["demanda"] >= 0:
            sucursales_validas.append(sucursal)
    return sucursales_validas

def distancia_entre_sucursales(poxicion_x_sucursal_uno, posicion_y_sucursal_uno, posicion_x_sucursal_dos, posicion_y_sucursal_dos):
    return ((poxicion_x_sucursal_uno - posicion_x_sucursal_dos)**2 + (posicion_y_sucursal_uno - posicion_y_sucursal_dos)**2)**(1/2)

def resolver(carga_actual, capacidad, sucursales, sucursales_visitadas, distancia_recorrida, sucursal_actual):
    sucursales_visitadas.append(sucursal_actual)
    if len(sucursales_visitadas) == len(sucursales):
        soluciones.append((sucursales_visitadas, distancia_recorrida))
        return True
    proximas_sucursales_validas = sucursales_validas(carga_actual, capacidad, sucursales, sucursales_visitadas)
    for sucursal in proximas_sucursales_validas:
        distancia_recorrida += distancia_entre_sucursales(sucursales[sucursal_actual[0]]["posicion_x"], sucursales[sucursal_actual[0]]["posicion_y"], sucursales[sucursal[0]]["posicion_x"], sucursales[sucursal[0]]["posicion_y"])
        carga_actual += sucursales[sucursal[0]]["demanda"]
        if resolver(carga_actual, capacidad, sucursales, sucursales_visitadas, distancia_recorrida, sucursal):
            return True
        else:
            print([x[0] for x in sucursales_visitadas])
            distancia_recorrida -= distancia_entre_sucursales(sucursales[sucursal_actual[0]]["posicion_x"], sucursales[sucursal_actual[0]]["posicion_y"], sucursales[sucursal[0]]["posicion_x"], sucursales[sucursal[0]]["posicion_y"])
            carga_actual -= sucursales[sucursal[0]]["demanda"]
            sucursales_visitadas.pop()
    return False

if __name__ == "__main__":
    main()