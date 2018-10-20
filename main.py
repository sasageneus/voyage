import os, sys
sys.path.append(os.path.dirname(__file__))
print(sys.path)

import table as table_py
import route as route_py
import state as state_py

route = route_py.Route()

n = 5 #количество пунктов в маршруте
point_names = ''.join(['%c' % x for x in range(97, 97+n)])  # gives 'abcdefghij'

state = state_py.first_state(point_names          
        , table_py.generate_random_distance(n, 9)
        )

for step in range(n - 3): #три последних шага отдельно выводим, так как там нет вариантов
    jump = state.next_zero_jump()
    route.append(jump)
    state = jump.state

route.print()    
