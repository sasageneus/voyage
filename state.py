import table
import copy as copy_py
from route import Jump

class FromPoint:
    name = None
    row = None
    min_dist = 0
    penalty = None
    def __init__(self, name, row)
        self.name = name
        self.min_dist = min(dist for dist in row if dist is not None)
        self.row = [dist - self.min_dist
                        if dist is not None else None
                            for dist in row]

    def find_penalty(self)
        self.penalty = min(dist for dist in row if dist) #Пропускаем ноли и None        


# Кортеж из трех позиций, описывает один пункт назначения, хранит по порядку
# 0 - name - наименование, 
# 1 - min - расстояние до ближайшего пункта, 
# 2 - penalty - размер штрафа если не воспользоваться ближайшим
def point_of(name):
    return (name, 0, 0)
def point_set_min(point, min_value):
    n, m, p = point
    return (n, min_value, p)
def point_set_penalty(point, penalty):
    n, m, p = point
    return (n, m, penalty)

class Point:
    min_dist = 0
    penalty = None
    def __init__(self, idx, name)
        self.idx = idx
        self.name = name
        
    def clone(self, idx):
        ret = Point(idx, self.name)
        ret.min_dist = self.min_dist

        return ret
        
    def minimaze(self, row):
        # находим минимальный при этом пропускаем неиспользуемые
        min_value = None
        for dist in row:
            if dist != None and (min_value == None or dist < min_value):
                min_value = dist

        assert(min_value != None)
        
        #Нормализуем, путем вычитания минимума из всех используемых ячеек
        ret_row = []
        for dist in row:
            if dist != None:
                ret_row.append(dist - min_value)
            else:
                ret_row.append(dist)

        self.min_dist += min_value

        return ret_row
        

def first_state(point_names, tbl):
    state = State()
    state.n = len(tbl)

    for i in range(state.n):
        point = Point(i, point_names[i])
        state.point_from.append(point)
        state.tbl.append(point.minimaze(tbl[i]))
        

    for j in range(state.n):
        point = Point(j, point_names[j])
        state.point_to.append(point)
        col = table.get_column(state.tbl, j)
        state.point_to.append(point)
        table.set_column(self.tbl, j, col_min)
    
    return state


#   Хранит текущее состояние и позволяет перейти в следующее
#   при этом порождает новый экземпляр State
class State:
    tbl = [] #таблица расстояний (приведенных к нулю)
    n = None #количество пуктов назначения
    cost = None #оценка минимально возможного маршрута это его расстояние определяется как Sum(point_from + point_to)
    point_from = [] #соответсвует строке i и содержит минимальное рассотояние из пункта i
    point_to = [] #соответсвует столбцу j и содержит минимальное добавочное рассотояние до пункта j
    zero = []

    #Создает новое состояние после перехода from_point -> to_point
    def new_state_after_jump(self, i, j):
        new_state = State()
        new_state.n = self.n - 1

        for i in range(n): 
            new_state.point_from.append(self.point_from[i])


    def normalize(self):
        self.n = len(tbl)

        #нормализуем строки
        for row in tbl:
            row_min, point_from[i] = minimaze(row)
            self.tbl.append(row_min)

        #нормализуем столбцы
        for j in range(self.n):
            col = table.get_column(self.tbl, j)
            col_min, point_to[j] = minimaze(col)
            table.set_column(self.tbl, j, col_min)

        #делаем оценку минимального маршрута
        self.cost = sum(point_from) + sum(point_to)

        #находим штрафы за неиспользование

    def next_zero_jump(self):
        jump = Jump()        
        raise Exception('Not supported')
