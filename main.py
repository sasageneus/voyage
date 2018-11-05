import os, sys
sys.path.append(os.path.dirname(__file__))
#print(sys.path)
import console
import distance
from route import Route
from state import State

#https://docs.python.org/3/library/contextlib.html
#https://preshing.com/20110920/the-python-with-statement-by-example/
#https://habr.com/post/337314/
#https://www.tutorialspoint.com/python/python_classes_objects.htm



#file_name = 'matrix'
#file_write = open(file_name + '.result', 'w')

def route_by_littl(point_names, tbl):
    n = len(point_names) #количество пунктов в маршруте
    state = State().begin(point_names, tbl)

    state.print()
    #print(state.zero)
    route = Route() #Здесь маршрут запоминаем (только один)

    for step in range(n - 2): #два последних шага отдельно выводим, так как там нет вариантов
        jump = state.next_zero_jump()
        route.append(jump)
        jump.print()
        print('')
        state = jump.state
        state.print()

    return route

#route = route_by_littl(*console.from_file('misha.input', distance.input_names_and_distance))
route = route_by_littl(*distance.random_distance(12))

route.finished() #найти два последних шага
route.print_chain()
print('')
route.print()
