_Hacer un informe explicando como funciona la eliminación de subtours en cada modelo, ventajas y desventajas de ambos, comparación de tiempos de corrida
Notar que el modelo MTZ tiene todas las variables Xij mientras que el otro tiene un "ordered" por lo tanto solo tiene Xij cuando i < j, ¿por que es posible esto?, ¿cuando no es posible?, ¿que beneficios tiene?
Para el modelo MTZ incluir el gráfico de la solapa "Statistics", usar los primeros 100 seg (a los 120seg comienza a hacer scroll y se pierde el comienzo), explicarlo_

_Un poco más de detalle: Comparar los modelos, uno es MTZ y el otro de eliminación de subtours, el primero lo conocen, el segundo agarra un subtour, agrega una restricción para eliminarlo y vuelve a correr hasta que no haya, la idea es comparar esos dos modelos_

# Eliminación de subtours 

Un subtuour se forma cuando el modelo recorre todas las sucursales, pero por más de un camino cerrado. Para evitar que se formen, se pueden especificamente eliminar todos los subtours posibles. Por ejemplo, si salgo de una sucursal hacia otra, no puedo volver de la segunda a la primera. En este caso se está eliminando un subtour de 2 sucursales. Si se quiere eliminar uno de tres sucursales debe procurarse que si se sale de **A** hacia **B** y de **B** hacia **C**, no se pueda ir de **C** a **A**. En terminos de programación lineal, si Y~ij~ es 1 si voy de la sucursal _i_ a la sucursal _j_, entonces:

Y~AB~ + Y~BC~ + Y~AC~ <= 2

Si se tienen `n` sucursales, se deben eliminar los subtours de hasta `n/2 - 1` sucursales. Esta forma de eliminación de subtours es más rápida que la de MTZ, pero la cantidad de restricciones que agraga al modelo lo vuelve impracticable en problemas con un número elevado de sucursales. Para el caso de eliminar subtours de hasta 2 sucursales, si se tienen 5 sucursales en total, se deben agregar 5 + 4 + 3 + 2 restricciones.

MTZ plantea entonces establecer un orden de visita entre las sucursales, agregando una variable por cada sucursal (el orden en que es visitada). De esta manera, restringe los subtours a partir del orden de visita, estableciendo que, si no se va de una sucursal a otra, la máxima diferencia entre estas debe ser menor a las cantidad de ciudades menos 1. Por el contrario, si se va de una a otra, obliga al modelo a que el orden de la segunda sea el siguiente al de la primera. Esto se plantea para cada par de sucursales. Se agregan restricciones, pero no tantas como en el caso anterior. Sin embargo, el tiempo es mucho mayor.

En nuestro caso, utilizando MTZ se alcanzó la solución luego de 320043.218 segundos, mientras que eliminando subtours fue de 28 segundos.

![Modelo MTZ](<statisticsMTZ.jpg>)



_Modificar la heurísitica desarrollada en la segunda entrega para que no tenga en cuenta las capacidades
Para los dos modelos agregar como solución inicial la obtenida mediante la heurística, la inserción de solución inicial ya está implementada (está comentada), agrega el camino trivial 1 --> 2 --> .... --> n --> 1 (constante "values") y se inserta mediante "cplex1.addMIPStart(opl.x,opl.values)", indicar que impacto tiene agregar la solución que obtuvieron y explicar el por qué.
Para el modelo MTZ incluir el gráfico de la solapa "Statistics", usar los primeros 100 seg (a los 120seg comienza a hacer scroll y se pierde el comienzo), explicar la diferencia al incluir la solución inicial_


44 71 45 4 68 91 13 74 31 27 49 72 80 14 77 15 78 59 16 79 88 94 10 63 48 73 76 87 1 98 34 30 84 7 8 89 96 35 93 52 33 92 54 46 90 56 26 75 18 85 65 55 58 50 70 86 29 81 25 20 51 43 67 32 23 38 41 57 39 60 66 17 11 61 36 69 24 12 53 40 42 9 28 6 37 2 19 99 47 83 97 100 5 95 82 3 62 22 21 64
TSP con la solucion inicial obtenida con la heuristica del problema dos: 30 segundos