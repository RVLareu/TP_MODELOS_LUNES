with open('ciudades_sin_demandas.txt', 'r') as file:
    lines = file.readlines()

lines_with_numbers = [lines[0]] + [f"{i} {line}" for i, line in enumerate(lines[1:], 1)]

with open('ciudades_con_numeros.txt', 'w') as file:
    file.writelines(lines_with_numbers)