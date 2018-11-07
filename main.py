import os, sys
sys.path.append(os.path.dirname(__file__))
#print(sys.path)
import console
import distance
from contextlib import redirect_stdout
from route import Route
from state import State
from bruteforce import Bruteforce

#https://docs.python.org/3/library/contextlib.html
#https://preshing.com/20110920/the-python-with-statement-by-example/
#https://habr.com/post/337314/
#https://www.tutorialspoint.com/python/python_classes_objects.htm

testpath = 'test/'

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


def resolve_by_littl(point_names, tbl):
    file_name = 'littl.output'
    file_write = open(file_name, 'w')

    with redirect_stdout(file_write):
        distance.print_names_and_distance(point_names, tbl)

    route = route_by_littl(point_names, tbl)
    route.finished() #найти два последних шага

    route.print_chain()
    print('')
    route.print()

    with redirect_stdout(file_write):
        route.print_chain()
        print('')
        route.print()

    file_write.close()

"""
point_names, tbl = console.from_file(testpath + 'misha.input', distance.input_names_and_distance)
resolve_by_littl(point_names, tbl)
assert(console.compare_files('littl.output', testpath + 'littl/misha.output'))

bf = Bruteforce(point_names, tbl)
bf.start('0')

#sys.exit(0)

point_names, tbl = console.from_file(testpath + 'test1.input', distance.input_names_and_distance)
resolve_by_littl(point_names, tbl)
assert(console.compare_files('littl.output', testpath + 'littl/test1.output'))

bf = Bruteforce(point_names, tbl)
bf.start('1')

#sys.exit(0)

point_names, tbl = console.from_file(testpath + 'test3zero.input', distance.input_names_and_distance)
resolve_by_littl(point_names, tbl)
assert(console.compare_files('littl.output', testpath + 'littl/test3zero.output'))

point_names, tbl = console.from_file(testpath + 'littl/big20.output', distance.input_names_and_distance)
resolve_by_littl(point_names, tbl)
assert(console.compare_files('littl.output', testpath + 'littl/big20.output'))
"""

point_names, tbl = distance.random_distance(11)
resolve_by_littl(point_names, tbl)

bf = Bruteforce(point_names, tbl)
bf.start('A')

#resolve_by_littl(*distance.random_distance(8))
