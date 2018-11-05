import console
import random

#Генерирует случайные расстояния между точками
def generate_random_distance(n, max_distance):
    tbl = [[None for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            tbl[i][j] = random.randint(1, max_distance)
            tbl[j][i] = tbl[i][j]

    return tbl



def random_distance(n):
    point_names = ''.join(['%c' % x for x in range(97, 97+n)])  # пункты назначения 'abcdefghij'
    rnd_tbl = generate_random_distance(n, 9)
    return point_names, rnd_tbl



def print_names(lst):
    for name in lst:
        print(name.rjust(5), end='')
    print('')


def print_distance(tbl):
    for row in tbl:
        for dist in row:
            print(str(dist if dist is not None else '-' ).rjust(5), end='')
        print('')
    print('')


def input_names_and_distance():
    point_names = input().split(' ')
    input()
    n = len(point_names)
    tbl = [[int(d) if d!='-' else None for d in input().split(' ')] for i in range(n)]

    print_names_and_distance(point_names, tbl)

    return point_names, tbl


#def load_from_file(filename):
def test_input_table_distance():
    input_table_distance()
#test_input_table_distance()


def print_names_and_distance(point_names, tbl):
    n = len(point_names)
    print_names(point_names)
    print (''.ljust(5 * n, '-'))
    print_distance(tbl)
    print('')
    print('')


def print_names_and_distance_test(n):
    unit.to_file('test_qweqew.input', lambda : print_names_and_distance(*random_distance(n)) )

#print_names_and_distance_test(5)

def input_names_and_distance_test():
    point_names, tbl = unit.from_file('misha.input', input_names_and_distance)
    print_names_and_distance(point_names, tbl)
#input_names_and_distance_test()