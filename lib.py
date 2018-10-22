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

def print_distance(tbl):
    for row in tbl:
        for dist in row:
            print('%s' % str(dist) if dist != None else '-' , end='\t')
        print('')
    print('')

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
