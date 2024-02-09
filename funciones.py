import random
import numpy as np
import copy
import interfaz as inter

def print_sudoku(board):
    for fila in board:
        print(' '.join(map(str, fila)))

def generar_sudoku(porcentaje):
    def es_valido(sudoku, fila, columna, num):
        # Verificar si el número es válido en la fila, columna y cuadrante
        for i in range(9):
            if sudoku[fila][i] == num or sudoku[i][columna] == num:
                return False
        
        start_row, start_col = 3 * (fila // 3), 3 * (columna // 3)
        for i in range(3):
            for j in range(3):
                if sudoku[i + start_row][j + start_col] == num:
                    return False
        
        return True

    def resolver_sudoku(sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    for num in range(1, 10):
                        if es_valido(sudoku, i, j, num):
                            sudoku[i][j] = num
                            if resolver_sudoku(sudoku):
                                return True
                            sudoku[i][j] = 0  # Si no es válido, se restaura
                    return False
        return True

    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    resolver_sudoku(sudoku)

    # Calcular la cantidad de celdas a eliminar según el porcentaje
    num_celdas_eliminar = int(81 * (100 - porcentaje) / 100)
    for _ in range(num_celdas_eliminar):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        sudoku[row][col] = 0

    return sudoku

def generar_poblacion_sudoku(desafio, tamano_poblacion):
    poblacion = []

    for _ in range(tamano_poblacion):
        nuevo_sudoku = [[num if num != 0 else random.randint(1, 9) for num in fila] for fila in desafio]
        poblacion.append(nuevo_sudoku)

    return poblacion


def tournamentSelection(population, tournament_size=2):
    selected_population = []
    random.seed()
    for _ in range(0, len(population), 2):
        tournament_participants1 = random.sample(population, tournament_size)
        tournament_participants2 = random.sample(population, tournament_size)
        tournament_fitness1 = [fitness_function(participante) for participante in tournament_participants1]
        tournament_fitness2 = [fitness_function(participante) for participante in tournament_participants2]
        winner1 = tournament_participants1[np.argmin(tournament_fitness1)]
        winner2 = tournament_participants2[np.argmin(tournament_fitness2)]
        selected_population.append([winner1, winner2])
    return selected_population

def crossOver(pc1, pc2, padres, population):
    nuevaPoblacion = []
    for i in range(0, len(padres)):
        p1 = population[-1]
        p2 = random.choice(population)

        rand1 = random.uniform(0, 1)
        if rand1 < pc1:  # Se realiza la cruza
            for r, row in enumerate(p1):
                rand2 = random.uniform(0, 1)
                if rand2 < pc2:  # Se realiza el intercambio de genes entre filas
                    for c, col in enumerate(row):
                        if col == 0:
                            p1[r][c], p2[r][c] = p2[r][c], p1[r][c]
            offspring1 = p1
            offspring2 = p2
        else:
            offspring1 = p1
            offspring2 = p2
        
        nuevaPoblacion.append(copy.deepcopy(offspring1))
        nuevaPoblacion.append(copy.deepcopy(offspring2))
                
    return nuevaPoblacion

def indexAvailableToSwap(row):
    index = [i for i, col in enumerate(row) if col == 0]
    if len(index) < 2:
        return None, None  # No hay suficientes celdas vacías para intercambiar
    index1, index2 = random.sample(index, 2)
    return index1, index2

def mutation(pm1, pm2, population):
    for individuo in population:
        for r, row in enumerate(individuo):
            rand1 = random.uniform(0, 1)
            if rand1 < pm1:
                idx1, idx2 = indexAvailableToSwap(row)
                if idx1 is not None and idx2 is not None:
                    row[idx1], row[idx2] = row[idx2], row[idx1]
            rand2 = random.uniform(0, 1)
            if rand2 < pm2:
                for c, col in enumerate(row):
                    if col == 0:
                        individuo[r][c] = 0
                sudoku = generar_sudoku(30)  # Ajusta el porcentaje según tu preferencia
                individuo[r] = sudoku[r]


def columnLocalSearch(population):
    for individuo in population:
        columnas_asociadas = []
        columnas = []
        repetidos = get_repeated_columns(individuo)
        nuevas_columnas = []

        for i in range(len(individuo)):
            columnas.append([row[i] for row in individuo])
            associated_column = [row[i] for row in individuo]
            columnas_asociadas.append(associated_column)

        for c, columna in enumerate(columnas):
            random_columna = random.choice(columnas)

            indice_col1 = columnas.index(columna)
            indice_col2 = columnas.index(random_columna)

            col_rep1 = repetidos[indice_col1]
            col_rep2 = repetidos[indice_col2]

            for r, row in enumerate(columna):
                if (col_rep1[r] == col_rep2[r] == 1) and (r not in columnas_asociadas[indice_col1]) and (r not in columnas_asociadas[indice_col2]):
                    if row != random_columna[r]:
                        temp = columna[r]
                        columna[r] = random_columna[r]
                        random_columna[r] = temp

            nuevas_columnas.append(list(columna))  # Dejar como lista

        for c, col in enumerate(nuevas_columnas):
            individuo = actualiza_columna(individuo, col, c)

def actualiza_columna(matriz, nueva_columna, indice_columna):
    nueva_matriz = [list(fila) for fila in matriz]
    for i in range(len(matriz)):
        nueva_matriz[i][indice_columna] = nueva_columna[i]
    return [tuple(fila) for fila in nueva_matriz]

def get_repeated_columns(sudoku):
    columns_repeated = np.zeros((len(sudoku), len(sudoku)), dtype=int)
    for i in range(len(sudoku)):
        column = [row[i] for row in sudoku]
        numeros = []
        repetidos = []
        for row in column:
            if row not in numeros:
                numeros.append(row)
            else:
                repetidos.append(row)
        for r, row in enumerate(column):
            if row in repetidos:
                columns_repeated[r][i] = 1
    return columns_repeated



def subblockLocalSearch(population):
    for individuo in population:
        subblocks = [individuo[i:i + 3] for i in range(0, 9, 3)]
        new_subblocks = []

        for index, subblock in enumerate(subblocks):
            random_subblock = random.choice(subblocks)
            rand_index = subblocks.index(random_subblock)

            for r, row in enumerate(subblock):
                actual_row = subblock[r]
                actual_row_rnd = random_subblock[r]
                repetidos = [1 if len(set(row)) < 3 else 0 for row in subblock]
                repetidos_rnd = [1 if len(set(row)) < 3 else 0 for row in random_subblock]

                if all(reps == 1 for reps in repetidos + repetidos_rnd):  # Hay repetidos
                    for c, valor in enumerate(row):
                        if valor != actual_row_rnd[c] and c not in range(3):
                            actual_row[c], actual_row_rnd[c] = actual_row_rnd[c], actual_row[c]

            new_subblocks.append(subblock)
       
        individuo[:] = [elemento for sublista in new_subblocks for elemento in sublista]

def sort_population(population):
    fitness_eval = [fitness_function(individuo) for individuo in population]
    sorted_population = [individuo for _, individuo in sorted(zip(fitness_eval, population), key=lambda x: x[0], reverse=True)]
    return sorted_population

def join_population(nueva, anterior, pop_size):
    nueva_poblacion = []
    for i in range(pop_size):
        individuo1 = fitness_function(nueva[i])
        individuo2 = fitness_function(anterior[i])
        if individuo1 < individuo2:
            nueva_poblacion.append(nueva[i])
        else:
            nueva_poblacion.append(anterior[i])
    return nueva_poblacion

def elite_population_learning(population, elite_population):
    elites = copy.deepcopy(elite_population)
    x_random = random.choice(elites)
    x_random_fitness = fitness_function(x_random)

    x_worst = population[0]
    max_fx = fitness_function(x_worst)
    Pb = (max_fx - x_random_fitness) / max_fx
    rand = random.uniform(0, 1)

    if rand < Pb:
        population[0] = x_random
    else:
        nuevo_individuo = generar_sudoku(30)  # Ajusta el porcentaje según tu preferencia
        population[0] = nuevo_individuo

def rellenar_ceros_sudokus(sudokus):
    sudokus_modificados = copy.deepcopy(sudokus)

    for sudoku in sudokus_modificados:
        for i in range(len(sudoku)):
            numeros_disponibles = set(range(1, 10))
            for j in range(len(sudoku[i])):
                if sudoku[i][j] == 0:
                    # Seleccionar un número aleatorio que aún no se ha utilizado en la fila
                    nuevo_numero = random.choice(list(numeros_disponibles))
                    sudoku[i][j] = nuevo_numero
                    numeros_disponibles.remove(nuevo_numero)
                else:
                    # Si el número ya está en la fila, quitarlo de los disponibles
                    numeros_disponibles.discard(sudoku[i][j])

    return sudokus_modificados

def fitness_function(X):
    n = 9
    contador = 0
    def contar_repetidos(memoria, inicio_i, fin_i, inicio_j, fin_j):
        nonlocal contador
        
        for i in range(inicio_i, fin_i):
            for j in range(inicio_j, fin_j):
                if X[j][i] == 0:
                    X[j][i] = random.randint(1,9)
                    if X[j][i] in memoria:
                        contador += 1
                    else:
                        memoria.append(X[j][i])
                else:
                    if X[j][i] in memoria:
                        contador += 1
                    else:
                        memoria.append(X[j][i])

    # Filas y columnas
    for i in range(n):
        memoria_filas = []
        memoria_columnas = []
        contar_repetidos(memoria_filas, i, i+1, 0, n)
        contar_repetidos(memoria_columnas, 0, n, i, i+1)

    # Cuadrantes
    for cuadrante_i in range(0, n, n//3):
        for cuadrante_j in range(0, n, n//3):
            memoria_cuadrante = []
            contar_repetidos(memoria_cuadrante, cuadrante_i, cuadrante_i + n//3, cuadrante_j, cuadrante_j + n//3)

    return contador

# x es el sodoku con el porcentaje de llenado 
def main(pc1, pc2, pm1, pm2, population_size, generaciones, x, y, flag):
    
    population = generar_poblacion_sudoku(y, population_size)
    
    if flag == 1:
        population[0] = x

    # Generaciones
    elite_population = []
    i = 0
    while i <= generaciones:
        i += 1
        padres = tournamentSelection(copy.deepcopy(population))

        nueva_poblacion = copy.deepcopy(population)
        
        nueva_poblacion = crossOver(pc1, pc2, padres, nueva_poblacion)

        mutation(pm1, pm2, nueva_poblacion)

        columnLocalSearch(nueva_poblacion)

        subblockLocalSearch(nueva_poblacion)

        nueva_poblacion = sort_population(copy.deepcopy(nueva_poblacion))
        poblacion_anterior = sort_population(copy.deepcopy(population))

        nueva_poblacion = join_population(copy.deepcopy(nueva_poblacion), copy.deepcopy(poblacion_anterior), population_size)

        best = copy.deepcopy(nueva_poblacion[-1])
        nobest = copy.deepcopy(nueva_poblacion[0])

        if all(fitness_function(best) < fitness_function(elite) for elite in elite_population):
            elite_population.append(copy.deepcopy(best))

        elite_population_learning(nueva_poblacion, copy.deepcopy(elite_population))

        #print(f"Best {fitness_function(best)}")

        population = copy.deepcopy(nueva_poblacion)
        
        if(fitness_function(best) == 0):
            print("Termine :O")
            return best, nobest
    
    return best, nobest

def mostrar_aptitud_poblacion(population):
    for p in population:
        print(f"{fitness_function(p)}", end='  ')
    print("\n")

def mostrar_pop(population):
    for p in population:
        print_sudoku(p)
    print("\n")

if __name__ == "__main__":
    main()