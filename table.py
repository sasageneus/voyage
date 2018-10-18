import random

def distance_of(value, used = True, worse = 0):
    return (value, used, worse)

#Генерирует случайные расстояния между точками
def generate_random_distance(n, max_distance):      
    tbl = []
    for i in range(n):
        tbl.append([])
        for j in range(n):
            tbl[i].append([])

    for i in range(n):
        tbl[i][i] = distance_of('-', False)
        for j in range(i + 1, n):
            tbl[i][j] = distance_of(random.randint(1, max_distance))
            tbl[j][i] = tbl[i][j]

    return tbl

def print_distance(tbl):
    for i in range(len(tbl)):
        for j in range(len(tbl[i])):
            v, u, w = tbl[i][j]
            print('%s' % str(v), end='\t')
        print('')
    print('')

def get_column(tbl, j):
    col = []
    for i in range(len(tbl)):
        col.append(tbl[i][j])
    
    return col

def set_column(tbl, j, column):
    for i in range(len(tbl)):
        tbl[i][j] = column[i]

def column_test():
    tbl = generate_random_distance(5, 9)
    print_distance(tbl)    
    col3 = get_column(tbl, 3)
    col1 = get_column(tbl, 1)
    #for i in range(len(tbl)):
     #   col[i] = distance_of(999)
    set_column(tbl, 1, col3)
    set_column(tbl, 3, col1)
    print_distance(tbl)    

#column_test()

def minimaze(row):
    #min_value = min([dist[0] for dist in row if dist[1] ]) 
    # находим минимальный при этом пропускаем неиспользуемые
    min_value = None
    for dist in row:
        v, u, w = dist
        if u and (min_value == None or v < min_value):
            min_value = v

    if min_value == None:
        min_value = 0 #Если все неиспользуются то 0 чтобы не повлиять на общую оценку

    #Нормализуем, путем вычитания минимума из всех используемых ячеек
    ret_row = []
    for dist in row:
        v, u, w = dist
        if u:
            ret_row.append(distance_of(v - min_value, u, w))
        else:
            ret_row.append(dist)

    return ret_row, min_value

def minimaze_test():
    tbl = generate_random_distance(5, 9)
    print_distance(tbl)    
    col, min_val = minimaze(get_column(tbl, 1))
    set_column(tbl, 1, col)
    print(min_val)
    print_distance(tbl)    

minimaze_test()

def copy(tbl):
    new_tbl = tbl.copy()
    for i in range(len(new_tbl)):
        new_tbl[i] = new_tbl[i].copy()

    return new_tbl


def copy_test():
    tbl = generate_random_distance(5, 9)

    new_tbl = copy(tbl)    
    assert(tbl[1][2] == new_tbl[1][2])

    new_tbl[1][2] = distance_of(*new_tbl[1][2])
    assert(tbl[1][2] == new_tbl[1][2])

    new_tbl[1][2] = distance_of(99)
    assert(tbl[1][2] != new_tbl[1][2])

    print_distance(tbl)    
    print('copy table:')
    print_distance(new_tbl)
    
#copy_test()
