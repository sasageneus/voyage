import random

#Генерирует случайные расстояния между точками
def generate_random_distance(n, max_distance):
    tbl = []
    for i in range(n):
        tbl.append([])
        for j in range(n):
            tbl[i].append([])

    for i in range(n):
        tbl[i][i] = None
        for j in range(i + 1, n):
            tbl[i][j] = random.randint(1, max_distance)
            tbl[j][i] = tbl[i][j]

    return tbl

def print_names(lst):
    for name in lst:
        print(name.rjust(5), end='')
    print('')

def print_distance(tbl):
    for row in tbl:
        for dist in row:
            print(str(dist if dist != None else '-' ).rjust(5), end='')
        print('')
    print('')


def input_table_distance():
    n = int(input())
    tbl = [[int(d) for d in input().split(' ')] for i in range(n)]

#def load_from_file(filename):
def test_input_table_distance():
    input_table_distance()

#test_input_table_distance()


#возвращает два наименьших по порядку
def min_and_penalty(row):
    m = None
    p = None
    for dist in row:
        if dist != None:
            if m == None or dist < m:
                p = m
                m = dist
            elif p == None or dist < p:
                p = dist
    assert(m != None)
    #assert(p != None)
    return m, p if p else 0

def minimaze(row):
    min_dist, penalty = min_and_penalty(row)
    if min_dist > 0:
        for i in range(len(row)):
            if row[i] != None:
                row[i] -= min_dist
        penalty -= min_dist
    return min_dist, penalty
