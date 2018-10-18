
import random

def set_distance(value, used = True, worse = 0):
    return (value, used, worse)

def simple_generator_distance_table(n, max_distance):
    tbl = []
    for i in range(n):
        tbl.append([])
        for j in range(n):
            tbl[i].append([])

    for i in range(n):
        tbl[i][i] = set_distance('-', False)
        for j in range(i + 1, n):
            tbl[i][j] = set_distance(random.randint(1, max_distance))
            tbl[j][i] = tbl[i][j]

    return tbl

def print_distance(tbl):
    for i in range(len(tbl)):
        for j in range(len(tbl[i])):
            v, u, w = tbl[i][j]
            print('%s' % str(v), end='\t')
        print('')


print_distance(simple_generator_distance_table(5, 9))
