import os, sys
sys.path.append(os.path.dirname(__file__))
#print(sys.path)
import lib
from route import Route
from state import State

n = 5 #количество пунктов в маршруте
file_name = 'matrix'
file_write = fopen(file_name + '.result', 'w')

#if file_name is None:
def random_distance(n):
    point_names = ''.join(['%c' % x for x in range(97, 97+n)])  # gives 'abcdefghij'

    rnd_tbl = lib.generate_random_distance(n, 9)

    return point_names, rnd_tbl

def print_matrix(out):
    lib.print_names(point_names)
    print (''.ljust(5 * n, '-'))
    lib.print_distance(rnd_tbl)
    print('')
    print('')

    if file_name not is None:
        stdio.



def simple_route(point_names, tbl):
    state = State().begin(point_names, tbl)

    state.print()
    #print(state.zero)
    route = Route() #Здесь маршрут запоминаем (только один)

    for step in range(n - 2): #три последних шага отдельно выводим, так как там нет вариантов
        print('step %d' % (step + 1))
        jump = state.next_zero_jump()
        route.append(jump)
        state = jump.state
        state.print()

    route.print()

simple_route(*random_distance(n))
