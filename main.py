import os, sys
sys.path.append(os.path.dirname(__file__))
#print(sys.path)

import table as table_py

from route import Route
from state import State

route = Route()

n = 5 #количество пунктов в маршруте
point_names = ''.join(['%c' % x for x in range(97, 97+n)])  # gives 'abcdefghij'

rnd_tbl = table_py.generate_random_distance(n, 9)

table_py.print_distance(rnd_tbl)
print('')
print('')

state = State().init(point_names, rnd_tbl)

state.print()
#print(state.zero)

for step in range(n - 2): #три последних шага отдельно выводим, так как там нет вариантов
    print('step %d' % (step + 1))
    jump = state.next_zero_jump()
    route.append(jump)
    state = jump.state
    state.print()

route.print()
