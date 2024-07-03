import heapq
import random

# Crear el mapa vacío (7x8)
map_ = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# Definir los costos de los obstáculos
COSTOS_OBSTACULOS = {
    '#': 2,  # Baches #
    '&': 3,  # Agua &
    '%': 999  # Edificio (no transitable) %
}

# Imprimir el mapa
def print_map(map_):
    symbols = {
        0: '.',  # camino libre
        '#': '#',  # Baches
        '&': '&',  # Agua
        '%': '%',  # Edificio
        'I': 'I',  # punto de inicio
        'S': 'S',  # punto de salida
        'R': 'R'  # ruta
    }
    
    for fila in map_:
        line = ""
        for element in fila:
            line += symbols.get(element, str(element)) + " "
        print(line)

# Agregar obstáculos
def add_obstacles(map_):
    while True:
        coordinate3 = input("Ingrese las coordenadas para agregar obstáculos separadas por un espacio, ej 0 0, o 'fin' para terminar: ").strip().lower()
        if coordinate3 == 'fin':
            break
        try:
            x, y = map(int, coordinate3.split())
            if x < 0 or x >= len(map_) or y < 0 or y >= len(map_[0]):
                print("Las coordenadas ingresadas están fuera del rango del mapa, por favor intente de nuevo")
                continue
            obstaculo = random.choice(['#', '&', '%'])
            map_[x][y] = obstaculo
        except (ValueError, IndexError):
            print("Entrada inválida, por favor ingrese dos números enteros válidos separados por un espacio")
            
# Definir punto de inicio
def start_point(map_):
    while True:
        try:
            coordinate1 = input("Ingrese las coordenadas de inicio separadas por un espacio, ej 0 0: ").strip().lower()
            x, y = map(int, coordinate1.split())
            if x < 0 or x >= len(map_) or y < 0 or y >= len(map_[0]):
                print("Las coordenadas ingresadas están fuera del rango del mapa, por favor intente de nuevo")
                continue
            if map_[x][y] in COSTOS_OBSTACULOS:
                print("Las coordenadas ingresadas son un obstáculo, por favor intente de nuevo")
                continue
            map_[x][y] = 'I'
            return (x, y)
        except (ValueError, IndexError):
            print("Entrada inválida, por favor ingrese dos números enteros válidos separados por un espacio")

# Definir punto de término
def end_point(map_):
    while True:
        try:
            coordinate2 = input("Ingrese las coordenadas de término separadas por un espacio, ej 0 0: ").strip().lower()
            x, y = map(int, coordinate2.split())
            if x < 0 or x >= len(map_) or y < 0 or y >= len(map_[0]):
                print("Las coordenadas ingresadas están fuera del rango del mapa, por favor intente de nuevo")
                continue
            if map_[x][y] in COSTOS_OBSTACULOS:
                print("Las coordenadas ingresadas son un obstáculo, por favor intente de nuevo")
                continue
            map_[x][y] = 'S'
            return (x, y)
        except (ValueError, IndexError):
            print("Entrada inválida, por favor ingrese dos números enteros válidos separados por un espacio")

# Función heurística que utiliza la distancia de Manhattan
def heuristic_function(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Obtener vecinos válidos 
def get_neighbors(pos, map_):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d in directions:
        neighbor = (pos[0] + d[0], pos[1] + d[1])
        if 0 <= neighbor[0] < len(map_) and 0 <= neighbor[1] < len(map_[0]) and map_[neighbor[0]][neighbor[1]] != '%':
            neighbors.append(neighbor)
    return neighbors

# Obtener costo de una posición
def get_cost(pos, map_):
    if map_[pos[0]][pos[1]] in COSTOS_OBSTACULOS:
        return COSTOS_OBSTACULOS[map_[pos[0]][pos[1]]]
    return 1  # Camino libre

# Algoritmo A*
def a_star(map_, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_function(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for neighbor in get_neighbors(current, map_):
            tentative_g_score = g_score[current] + get_cost(neighbor, map_)
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_function(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return None

# Mostrar el mapa original
print("Mapa original: ")
print_map(map_)

# Agregar obstáculos al mapa
add_obstacles(map_)

# Mostrar el mapa final con obstáculos
print("Mapa final con obstáculos:")
print_map(map_)

# Obtener el punto de inicio del mapa
start = start_point(map_)

# Obtener el punto final del mapa
goal = end_point(map_)

# Mostrar el mapa actualizado con el punto de inicio y salida
print("Mapa con el punto de inicio y salida:")
print_map(map_)

# Encontrar la ruta más rápida usando A*
path = a_star(map_, start, goal)

# Mostrar el camino encontrado
if path:
    for paso in path:
        if map_[paso[0]][paso[1]] == 0:
            map_[paso[0]][paso[1]] = 'R'
    print("Mapa con la ruta más rápida:")
    print_map(map_)
else:
    print("No se encontró un camino desde el inicio hasta la meta.")
